import logging
from utils.memory import read, get_flag
from utils.alpaca_client import get_account
from config import (
    MAX_POSITION_PCT, DAILY_LOSS_CAP_PCT, MAX_TRADES_PER_DAY,
    MIN_RESEARCH_SCORE, MIN_VOLUME_MULTIPLIER, MAX_VIX, ALLOW_OPTIONS,
)

log = logging.getLogger(__name__)


class RiskManager:
    def __init__(self):
        self.account = None

    def load_account(self):
        self.account = get_account()
        return self.account

    def is_halted(self):
        halt = get_flag("weekly_trade_counter.md", "daily_loss_halt")
        return halt and halt.lower() == "true"

    def daily_trades_remaining(self):
        val = get_flag("weekly_trade_counter.md", "trades_this_week")
        used = int(val) if val and val.isdigit() else 0
        return MAX_TRADES_PER_DAY - used

    def portfolio_value(self):
        if not self.account:
            self.load_account()
        return float(self.account["equity"])

    def max_position_dollars(self):
        return self.portfolio_value() * MAX_POSITION_PCT

    def daily_pnl_pct(self):
        if not self.account:
            self.load_account()
        equity = float(self.account["equity"])
        last_equity = float(self.account["last_equity"])
        return (equity - last_equity) / last_equity

    def check_daily_loss(self):
        pnl = self.daily_pnl_pct()
        if pnl <= -DAILY_LOSS_CAP_PCT:
            return False, pnl
        return True, pnl

    def approve_entry(self, symbol, score, volume_ratio, vix, spy_ok, asset_class="us_equity"):
        reasons = []

        if not ALLOW_OPTIONS and asset_class not in ("us_equity", "equity"):
            reasons.append(f"asset class '{asset_class}' not allowed (stocks only)")

        if self.is_halted():
            reasons.append("daily loss halt is active")

        if self.daily_trades_remaining() <= 0:
            reasons.append(f"daily trade limit ({MAX_TRADES_PER_DAY}) reached")

        ok, pnl = self.check_daily_loss()
        if not ok:
            reasons.append(f"daily P&L {pnl:.2%} exceeds -{DAILY_LOSS_CAP_PCT:.0%} cap")

        if score < MIN_RESEARCH_SCORE:
            reasons.append(f"research score {score} < minimum {MIN_RESEARCH_SCORE}")

        if volume_ratio < MIN_VOLUME_MULTIPLIER:
            reasons.append(f"volume ratio {volume_ratio:.1f}x < minimum {MIN_VOLUME_MULTIPLIER}x")

        if vix >= MAX_VIX:
            reasons.append(f"VIX {vix:.1f} >= max allowed {MAX_VIX}")

        if not spy_ok:
            reasons.append("SPY below 5-day MA — market not in uptrend")

        if reasons:
            log.info(f"[RiskManager] BLOCKED {symbol}: {'; '.join(reasons)}")
            return False, reasons

        log.info(f"[RiskManager] APPROVED {symbol}")
        return True, []

    def shares_to_buy(self, price):
        max_dollars = self.max_position_dollars()
        shares = int(max_dollars / price)
        return max(shares, 1)
