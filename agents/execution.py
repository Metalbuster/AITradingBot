import logging
from utils import memory, github_sync
from utils.alpaca_client import (
    place_limit_order, place_stop_limit_order,
    get_latest_bar, close_position,
)
from utils.email_client import send_trade_alert
from config import STOP_LOSS_DEFAULT_PCT, STOP_LOSS_HIGH_BETA_PCT, ALLOW_OPTIONS, MAX_TRADES_PER_DAY

log = logging.getLogger(__name__)


def open_trade(symbol, score, thesis, technical, shares):
    price = technical["price"]
    high_beta = technical.get("high_beta", False)
    stop_pct = STOP_LOSS_HIGH_BETA_PCT if high_beta else STOP_LOSS_DEFAULT_PCT
    stop_price = round(price * (1 - stop_pct), 2)
    stop_limit = round(stop_price * 0.995, 2)

    t1 = round(price * 1.08, 2)
    t2 = round(price * 1.15, 2)
    t3 = round(price * 1.25, 2)
    shares_t1 = max(1, round(shares * 0.33))
    shares_t2 = max(1, round(shares * 0.33))
    shares_t3 = shares - shares_t1 - shares_t2

    order = place_limit_order(symbol, shares, "buy", price)
    log.info(f"[Execution] BUY order placed: {symbol} {shares}sh @ ${price:.2f} | order_id={order.get('id')}")

    place_stop_limit_order(symbol, shares, "sell", stop_price, stop_limit)
    log.info(f"[Execution] Stop-limit placed for {symbol} @ ${stop_price:.2f}")

    position_entry = (
        f"\n## {symbol} — Opened {memory.now_et()}\n"
        f"- Entry: ${price:.2f} | Shares: {shares} | Cost: ${price * shares:.2f}\n"
        f"- Stop-loss: ${stop_price:.2f} ({stop_pct:.0%} below entry)\n"
        f"- Target 1: ${t1:.2f} (+8%) — sell {shares_t1} shares\n"
        f"- Target 2: ${t2:.2f} (+15%) — sell {shares_t2} shares\n"
        f"- Target 3: ${t3:.2f} (+25%) — sell {shares_t3} shares\n"
        f"- Thesis: {thesis}\n"
        f"- Research score: {score}/100\n"
        f"- High-beta: {high_beta}\n"
    )
    memory.append("open_positions.md", position_entry)

    trade_row = f"| {memory.today_et()} | {symbol} | ${price:.2f} | open | {shares} | — | — | {thesis[:60]} |"
    memory.append("trade_log.md", trade_row)

    counter_val = memory.get_flag("weekly_trade_counter.md", "trades_this_week")
    used = int(counter_val) if counter_val and counter_val.isdigit() else 0
    memory.set_flag("weekly_trade_counter.md", "trades_this_week", str(used + 1))
    memory.set_flag("weekly_trade_counter.md", "trades_remaining", str(MAX_TRADES_PER_DAY - used - 1))

    memory.append(
        "weekly_trade_counter.md",
        f"- {memory.today_et()}: BUY {symbol} @ ${price:.2f} (counted)"
    )

    journal = (
        f"## {memory.now_et()}\n"
        f"Bought {shares} shares of {symbol} @ ${price:.2f}. Score: {score}/100. "
        f"Stop: ${stop_price:.2f}. Targets: ${t1}/${t2}/${t3}. Thesis: {thesis}\n---"
    )
    memory.append("reasoning.md", journal)

    send_trade_alert("BUY", symbol, shares, price, stop_price, thesis, score)
    github_sync.push(f"auto: BUY {symbol} {shares}sh @ ${price:.2f} | score:{score}")
    return order


def close_trade(symbol, reason="manual"):
    try:
        result = close_position(symbol)
        log.info(f"[Execution] Closed {symbol}: {reason}")
        journal = (
            f"## {memory.now_et()}\n"
            f"Closed {symbol}. Reason: {reason}.\n---"
        )
        memory.append("reasoning.md", journal)
        github_sync.push(f"auto: CLOSE {symbol} | reason: {reason}")
        return result
    except Exception as e:
        log.error(f"[Execution] Failed to close {symbol}: {e}")
        return None
