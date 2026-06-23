import re
import logging
from utils import memory, github_sync
from utils.alpaca_client import get_positions, get_account, close_position, get_latest_bar
from utils.email_client import send_stop_loss_alert, send_halt_alert
from config import DAILY_LOSS_CAP_PCT, TRAILING_STOP_PCT, MAX_TRADES_PER_DAY

log = logging.getLogger(__name__)

_intraday_highs = {}


def check_daily_halt():
    account = get_account()
    equity = float(account["equity"])
    last_equity = float(account["last_equity"])
    pnl_pct = (equity - last_equity) / last_equity

    if pnl_pct <= -DAILY_LOSS_CAP_PCT:
        log.warning(f"[Monitor] Daily loss cap hit: {pnl_pct:.2%} — halting all routines")
        memory.set_flag("weekly_trade_counter.md", "daily_loss_halt", "true")
        memory.set_flag("weekly_trade_counter.md", "halt_reason", f"Daily loss {pnl_pct:.2%}")
        memory.set_flag("weekly_trade_counter.md", "halt_date", memory.today_et())
        send_halt_alert(f"Daily loss {pnl_pct:.2%}", equity, pnl_pct)
        journal = (
            f"## {memory.now_et()}\n"
            f"HALT triggered. Portfolio down {pnl_pct:.2%} today (cap: -{DAILY_LOSS_CAP_PCT:.0%}). "
            f"All routines suspended for today.\n---"
        )
        memory.append("reasoning.md", journal)
        github_sync.push(f"auto: HALT triggered | daily loss {pnl_pct:.2%}")
        return True, pnl_pct
    return False, pnl_pct


def _parse_open_positions():
    content = memory.read("open_positions.md")
    positions = {}
    for block in re.split(r"\n## ", content):
        symbol_m = re.match(r"([A-Z]+)\s*—", block)
        if not symbol_m:
            continue
        symbol = symbol_m.group(1)
        entry_m = re.search(r"Entry:\s*\$([0-9.]+)", block)
        stop_m = re.search(r"Stop-loss:\s*\$([0-9.]+)", block)
        t1_m = re.search(r"Target 1:\s*\$([0-9.]+).*?sell (\d+)", block)
        t2_m = re.search(r"Target 2:\s*\$([0-9.]+).*?sell (\d+)", block)
        t3_m = re.search(r"Target 3:\s*\$([0-9.]+).*?sell (\d+)", block)
        thesis_m = re.search(r"Thesis:\s*(.+)", block)
        if entry_m and stop_m:
            positions[symbol] = {
                "entry": float(entry_m.group(1)),
                "stop": float(stop_m.group(1)),
                "t1": (float(t1_m.group(1)), int(t1_m.group(2))) if t1_m else None,
                "t2": (float(t2_m.group(1)), int(t2_m.group(2))) if t2_m else None,
                "t3": (float(t3_m.group(1)), int(t3_m.group(2))) if t3_m else None,
                "thesis": thesis_m.group(1).strip() if thesis_m else "",
            }
    return positions


def run():
    log.info("[Monitor] Intraday check running")

    halted, pnl_pct = check_daily_halt()
    if halted:
        positions = get_positions()
        for p in positions:
            close_position(p["symbol"])
            log.info(f"[Monitor] Force-closed {p['symbol']} due to daily halt")
        return

    open_mem = _parse_open_positions()
    live_positions = {p["symbol"]: p for p in get_positions()}

    for symbol, mem_pos in open_mem.items():
        if symbol not in live_positions:
            continue

        bar = get_latest_bar(symbol)
        current_price = float(bar.get("c", 0))
        if not current_price:
            continue

        if symbol not in _intraday_highs or current_price > _intraday_highs[symbol]:
            _intraday_highs[symbol] = current_price

        intraday_high = _intraday_highs[symbol]
        trailing_stop = round(intraday_high * (1 - TRAILING_STOP_PCT), 2)
        entry = mem_pos["entry"]
        gain_pct = (current_price - entry) / entry

        log.info(
            f"[Monitor] {symbol}: current=${current_price:.2f} entry=${entry:.2f} "
            f"gain={gain_pct:.2%} intraday_high=${intraday_high:.2f}"
        )

        t1 = mem_pos.get("t1")
        if t1 and current_price >= t1[0]:
            if gain_pct >= 0.08 and current_price < intraday_high * (1 - TRAILING_STOP_PCT):
                log.info(f"[Monitor] {symbol} hit trailing stop after T1: ${current_price:.2f}")
                close_position(symbol)
                pnl = (current_price - entry) * int(live_positions[symbol]["qty"])
                send_stop_loss_alert(symbol, entry, current_price, int(live_positions[symbol]["qty"]), pnl)
                journal = (
                    f"## {memory.now_et()}\n"
                    f"Trailing stop hit for {symbol} @ ${current_price:.2f} "
                    f"({gain_pct:.2%} gain). Intraday high was ${intraday_high:.2f}.\n---"
                )
                memory.append("reasoning.md", journal)

    github_sync.push("auto: intraday monitor check")
    log.info("[Monitor] Done")


def reset_daily_halt():
    halt = memory.get_flag("weekly_trade_counter.md", "daily_loss_halt")
    if halt and halt.lower() == "true":
        memory.set_flag("weekly_trade_counter.md", "daily_loss_halt", "false")
        memory.set_flag("weekly_trade_counter.md", "halt_reason", "")
        log.info("[Monitor] Daily halt flag reset for new trading day")
        github_sync.push("auto: daily halt reset — new trading day")


def reset_daily_counter():
    memory.set_flag("weekly_trade_counter.md", "trades_this_week", "0")
    memory.set_flag("weekly_trade_counter.md", "trades_remaining", str(MAX_TRADES_PER_DAY))
    log.info("[Monitor] Daily trade counter reset")
    github_sync.push("auto: daily trade counter reset — new trading day")
