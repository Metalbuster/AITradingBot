# AITradingBot — Claude Code Context

## What This Project Is
An automated stock trading bot that:
- Researches stocks via **Perplexity AI**
- Trades on **Alpaca** (paper trading by default)
- Sends reports to **jankla2010@gmail.com** via Gmail SMTP
- Runs on a schedule via **Claude desktop local routines**
- Stores all state in **local `.md` memory files** (also synced to GitHub)

---

## Project Structure

```
d:\AITradingBot\
├── CLAUDE.md              ← you are here
├── MANUAL.md              ← plain-English guide for the user
├── CHANGELOG.md           ← version history
├── main.py                ← Python scheduler (local fallback runner)
├── run_bot.bat            ← Windows one-click launcher
├── config.py              ← all constants and hard rule values
├── .env                   ← real credentials (gitignored, never commit)
├── .env.example           ← template with placeholders
├── agents/                ← Python agent modules
│   ├── coordinator.py     ← orchestrates all agents, reads strategy.md first
│   ├── research.py        ← Perplexity AI queries
│   ├── technical.py       ← Alpaca market data
│   ├── risk_manager.py    ← enforces all hard rules
│   ├── execution.py       ← Alpaca order placement
│   ├── monitor.py         ← intraday stop-loss / take-profit checks
│   ├── reporter.py        ← email reports via Gmail SMTP
│   └── benchmark.py       ← portfolio vs SPY tracking
├── utils/
│   ├── alpaca_client.py   ← Alpaca REST API wrapper
│   ├── perplexity_client.py ← Perplexity AI API wrapper
│   ├── email_client.py    ← Gmail SMTP wrapper
│   ├── github_sync.py     ← git pull/push (disabled in local mode)
│   └── memory.py          ← read/write/append .md memory files
├── memory/                ← THE BOT'S BRAIN — all state lives here
│   ├── strategy.md        ← ★ MASTER RULES — read first on every run
│   ├── watchlist.md       ← stocks + inverse ETFs being monitored
│   ├── research_cache.md  ← latest Perplexity scores per ticker
│   ├── daily_context.md   ← today's SPY trend, VIX, sector leaders
│   ├── open_positions.md  ← all currently held positions
│   ├── trade_log.md       ← complete trade history
│   ├── portfolio_state.md ← current cash, equity, daily P&L
│   ├── weekly_trade_counter.md ← daily trade count + halt flags
│   ├── benchmark_tracking.md   ← portfolio vs SPY over time
│   ├── performance_metrics.md  ← win rate, profit factor, all-time stats
│   ├── learned_patterns.md     ← weekly reflections on what worked
│   ├── reasoning.md            ← append-only journal of every decision
│   ├── risk_rules.md           ← editable numerical thresholds
│   ├── news_events.md          ← upcoming earnings, Fed dates
│   └── pending_orders.md       ← orders awaiting fill
└── .claude/
    └── commands/          ← Claude skills (slash commands)
        ├── research.md    ← /research
        ├── trade.md       ← /trade
        ├── journal.md     ← /journal
        ├── benchmark.md   ← /benchmark
        └── report.md      ← /report
```

---

## Hard Rules (enforced in code — do not bypass)

| Rule | Value | Where enforced |
|---|---|---|
| Max position size | 5% of portfolio (3% for SH) | `config.py`, `risk_manager.py`, `/trade` skill |
| Daily loss halt | -2% stops all trading for the day | `monitor.py`, `coordinator.py` |
| Max trades per day | 3 | `config.py`, `risk_manager.py` |
| No options | Stocks + approved ETFs only | `risk_manager.py`, `/trade` skill |
| Paper trading | Until `live_trading: true` in strategy.md | `coordinator.py` |

---

## Entry Criteria (all must be true)

- Research score ≥ 70/100 (60/100 for SH inverse ETF)
- Volume ≥ 1.25x 30-day average
- SPY above 5-day MA (or below MA → evaluate SH instead)
- VIX < 28
- Daily trade count < 3
- Daily portfolio loss < 2%

---

## Key Config Values (`config.py`)

```python
MAX_POSITION_PCT = 0.05        # 5% per trade
DAILY_LOSS_CAP_PCT = 0.02      # -2% halt
MAX_TRADES_PER_DAY = 3
MIN_RESEARCH_SCORE = 70
MIN_VOLUME_MULTIPLIER = 1.25
MAX_VIX = 28.0
SYNC_TO_GITHUB = False         # set True to re-enable git push/pull
```

---

## Daily Routine Schedule (Bangkok time / ICT)

| Time | Routine | What It Does |
|---|---|---|
| 7:33 PM Mon–Fri | pre-market-research | Perplexity scan, score all watchlist tickers |
| 8:37 PM Mon–Fri | market-open | Evaluate scores, place trades if all criteria pass |
| 8:30–11:30 PM Mon–Fri | intraday-monitor (x4) | Check stop-loss and take-profit on open positions |
| 2:47 AM Tue–Sat | eod | Close weak positions, send email report, reset daily counter |
| 4:23 AM Saturdays | weekly-summary | Full week recap, email sent, performance metrics updated |

---

## Inverse ETF Mode (SH)

When SPY is below its 5-day MA, regular stock entries are blocked.
The bot instead evaluates **SH** (1x inverse SPY ETF):
- Entry threshold: score ≥ 60
- Position size: 3% of portfolio max
- Exit: immediately when SPY reclaims 5-day MA
- No leveraged inverse ETFs (SQQQ, SPXS, etc.)

---

## Current Status

- **Mode:** Paper trading (`live_trading: false` in memory/strategy.md)
- **Starting balance:** $100,000 (Alpaca default)
- **Live since:** 2026-06-17
- **Trades executed:** 1 (NVDA, -$126.63, closed same day)
- **GitHub repo:** github.com/Metalbuster/AITradingBot (public)

---

## How to Make Changes

### Tune thresholds (no code needed)
Edit `memory/risk_rules.md` directly. Changes take effect on the next routine run.

### Change hard rules
Edit `config.py`. The constants there are the source of truth for the Python agents.
Also update `memory/strategy.md` to keep the documentation in sync.

### Add a new skill
Create a new `.md` file in `.claude/commands/`. Name it after the slash command.

### Enable GitHub sync
Set `SYNC_TO_GITHUB = True` in `config.py`.

### Switch to live trading
1. Change `live_trading: false` → `live_trading: true` in `memory/strategy.md`
2. Update `.env` with live Alpaca API keys (not paper keys)

---

## What NOT to Do

- Never commit `.env` — it contains real API keys
- Never set `live_trading: true` without at least 4 weeks of paper trading results
- Never add options trading — `ALLOW_OPTIONS = False` is a hard rule
- Never edit `memory/reasoning.md` manually — it is append-only
