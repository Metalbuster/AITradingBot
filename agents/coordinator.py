import re
import logging
from utils import memory, github_sync
from utils.alpaca_client import get_account, get_positions
from agents import research as research_agent
from agents import technical as technical_agent
from agents.risk_manager import RiskManager
from agents import execution as execution_agent
from agents import monitor as monitor_agent
from agents import reporter as reporter_agent

log = logging.getLogger(__name__)


def _read_strategy():
    return memory.read("strategy.md")


def _is_live():
    strategy = _read_strategy()
    m = re.search(r"live_trading:\s*(true|false)", strategy, re.IGNORECASE)
    return m and m.group(1).lower() == "true"


def _parse_research_cache():
    content = memory.read("research_cache.md")
    candidates = []
    for block in re.split(r"\n## ", content):
        m = re.match(r"([A-Z]+)\s*\|\s*Score:\s*(\d+)/100", block)
        if m:
            symbol = m.group(1)
            score = int(m.group(2))
            thesis_m = re.search(r"Catalyst:\s*(.+)", block)
            thesis = thesis_m.group(1).strip() if thesis_m else "See research cache"
            candidates.append((symbol, score, thesis))
    return sorted(candidates, key=lambda x: x[1], reverse=True)


def run_pre_market(tickers=None):
    log.info("[Coordinator] Pre-market run starting")
    github_sync.pull()
    strategy = _read_strategy()
    log.info("[Coordinator] strategy.md loaded")

    if memory.get_flag("weekly_trade_counter.md", "daily_loss_halt") == "true":
        log.info("[Coordinator] Halt flag set — skipping pre-market research")
        return

    research_agent.run(tickers=tickers)
    log.info("[Coordinator] Pre-market research complete")


def run_market_open(tickers=None):
    log.info("[Coordinator] Market open run starting")
    github_sync.pull()
    strategy = _read_strategy()

    risk = RiskManager()
    risk.load_account()

    if risk.is_halted():
        log.info("[Coordinator] Halted — no trades today")
        return

    if risk.daily_trades_remaining() <= 0:
        log.info("[Coordinator] Daily trade limit reached — no new entries")
        return

    ok, pnl = risk.check_daily_loss()
    if not ok:
        log.info(f"[Coordinator] Daily loss cap hit ({pnl:.2%}) — no trades")
        return

    candidates = _parse_research_cache()
    live_positions = {p["symbol"] for p in get_positions()}

    for symbol, score, thesis in candidates:
        if symbol in live_positions:
            log.info(f"[Coordinator] {symbol} already held — skipping")
            continue

        tech = technical_agent.analyze(symbol)
        if not tech or not tech["technically_sound"]:
            log.info(f"[Coordinator] {symbol} failed technical check")
            continue

        context = memory.read("daily_context.md")
        vix_m = re.search(r"VIX[:\s]+(\d+\.?\d*)", context, re.IGNORECASE)
        vix = float(vix_m.group(1)) if vix_m else 20.0
        spy_ok = "above" in context.lower()

        approved, reasons = risk.approve_entry(
            symbol, score, tech["volume_ratio"], vix, spy_ok
        )
        if not approved:
            continue

        shares = risk.shares_to_buy(tech["price"])
        execution_agent.open_trade(symbol, score, thesis, tech, shares)

        if risk.daily_trades_remaining() <= 0:
            log.info("[Coordinator] Daily trade limit now reached — stopping")
            break

    log.info("[Coordinator] Market open run complete")


def run_intraday():
    log.info("[Coordinator] Intraday monitor run")
    github_sync.pull()

    if memory.get_flag("weekly_trade_counter.md", "daily_loss_halt") == "true":
        log.info("[Coordinator] Halted — skipping intraday monitor")
        return

    monitor_agent.run()


def run_eod():
    log.info("[Coordinator] EOD run")
    github_sync.pull()

    account = get_account()
    equity = float(account["equity"])
    last_equity = float(account["last_equity"])
    daily_pnl = equity - last_equity
    daily_pnl_pct = daily_pnl / last_equity

    portfolio_content = (
        f"# Portfolio State\nLast updated: {memory.now_et()}\n\n"
        f"- Cash available: ${float(account['cash']):,.2f}\n"
        f"- Invested: ${float(account['long_market_value']):,.2f}\n"
        f"- Total equity: ${equity:,.2f}\n"
        f"- Daily P&L: ${daily_pnl:+,.2f} ({daily_pnl_pct:+.2%})\n"
        f"- Open positions: {len(get_positions())}\n"
    )
    memory.write("portfolio_state.md", portfolio_content)

    reporter_agent.run_eod()
    monitor_agent.reset_daily_halt()
    monitor_agent.reset_daily_counter()
    log.info("[Coordinator] EOD complete")


def run_weekly_summary():
    log.info("[Coordinator] Weekly summary run")
    github_sync.pull()
    reporter_agent.run_weekly()


def run_benchmark():
    from agents import benchmark as benchmark_agent
    github_sync.pull()
    benchmark_agent.run()
