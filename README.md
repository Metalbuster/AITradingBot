# AITradingBot — User Manual

A plain-English guide to how the bot works, what it does, and all the rules it follows.

---

## What This Bot Does

The bot monitors the US stock market every day and automatically:
1. Researches stocks using AI (Perplexity)
2. Decides whether to buy based on a strict set of rules
3. Monitors open positions every hour and exits when targets are hit
4. Sends you an end-of-day email report
5. Keeps a journal of every decision it makes

All trading happens on **Alpaca** (currently paper trading — fake money, no real risk).

---

## Getting Started (New User Setup)

### 1. Prerequisites
- Python 3.10+
- A GitHub repo for this project (used to back up `memory/` state — see [Backup & Syncing](#backup--syncing))
- Accounts on: [Alpaca](https://alpaca.markets) (paper trading), [Perplexity AI](https://www.perplexity.ai) (research), Gmail (reports)

### 2. Install dependencies
```
pip install -r requirements.txt
```
This installs `alpaca-py`, `anthropic`, `gitpython`, `python-dotenv`, `requests`, `pytz`, and `schedule`.

### 3. Configure credentials
Copy `.env.example` to `.env` and fill in your real values — **never commit `.env`**:

| Variable | Where to get it |
|---|---|
| `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` | Alpaca dashboard → Paper Trading → API Keys. Leave `ALPACA_BASE_URL` pointed at `paper-api.alpaca.markets` until you're ready to go live |
| `PERPLEXITY_API_KEY` | Perplexity AI account → API settings |
| `EMAIL_SENDER` / `EMAIL_PASSWORD` | A Gmail address + an [App Password](https://support.google.com/accounts/answer/185833) (not your real Gmail password) |
| `EMAIL_RECIPIENT` | Where reports get sent (defaults to `jankla2010@gmail.com` if unset) |
| `GITHUB_TOKEN` / `GITHUB_REPO` / `GITHUB_BRANCH` | A GitHub personal access token with repo write access, and the `owner/repo` this bot's `memory/` files sync to |

### 4. Start the bot
```
python main.py
```
This starts a long-running scheduler loop (see `main.py`) — it does **not** trade immediately. It registers the routines below and checks every 30 seconds whether one is due, plus polls `memory/trade_trigger.md` every 30 seconds for manual trade requests. Leave it running (e.g. in a background terminal, `screen`/`tmux` session, or as a service) for it to operate on schedule. Logs go to `logs/bot.log` and stdout.

### 5. Verify it's working
- Check `logs/bot.log` for `"AI Trading Bot starting up"` and routine log lines
- After the next scheduled pre-market research run, check `memory/research_cache.md` for scored tickers
- You should receive an EOD email report the same day trading starts

### 6. What to expect on day one
- The bot starts in **paper trading mode** (`live_trading: false` in `memory/strategy.md`) — no real money is at risk
- It won't necessarily place a trade on the first run — entries only happen when [all 5 entry rules](#the-5-rules-before-any-trade) pass
- Read the rest of this manual (below) to understand what it's doing and why before you consider flipping it to live trading

> **Note on times:** `main.py`'s schedule is written in US Eastern Time (ET) — e.g. `08:33`, `09:37`, `15:47`. The [Daily Schedule](#daily-schedule-bangkok-time--ict) section below describes the same routines converted to Bangkok time (ICT) for reference.

---

## Key Terms Explained

| Term | What It Means |
|---|---|
| **SPY** | An ETF that tracks the 500 biggest US companies. It goes up when the overall market goes up. Used as the market's health indicator. |
| **VIX** | The "Fear Gauge." Measures how nervous investors are. Low VIX (< 20) = calm market. High VIX (> 28) = fearful, choppy market — bot avoids trading. |
| **5-day MA** | Moving Average — the average price of SPY over the last 5 trading days. If today's SPY price is above this average, the market is in an uptrend. |
| **Volume** | How many shares of a stock are traded today vs the normal daily amount. High volume = big investors are active in that stock. |
| **Stop-loss** | A safety net price. If the stock falls this far below your buy price, the bot sells automatically to cut the loss. |
| **Take-profit** | A target price. When the stock rises this much, the bot sells a portion to lock in gains. |
| **Paper trading** | Trading with fake money to test the strategy. Works exactly like real trading but no real money at risk. |
| **ETF** | Exchange Traded Fund — a basket of stocks you can buy as a single share. SPY holds all 500 S&P 500 stocks. |
| **Inverse ETF** | An ETF that moves opposite to the market. When SPY goes down 1%, SH goes up 1%. Used to profit during market downturns. |
| **Research score** | A score from 0–100 the bot assigns each stock after analyzing news, analyst opinions, volume, and technical charts. |
| **Portfolio** | Your total account value — cash + value of stocks currently held. |
| **Equity** | Another word for your total portfolio value (cash + investments). |
| **Alpha** | How much better (or worse) you did vs SPY. +1% alpha means you beat the market by 1% that day. |

---

## Daily Schedule (Bangkok Time / ICT)

| Time | What Happens |
|---|---|
| **7:33 PM** (Mon–Fri) | Pre-market research — bot scans all watchlist stocks, scores them 0–100 |
| **8:37 PM** (Mon–Fri) | Market open — bot reviews scores and places trades if conditions are met |
| **8:30 PM, 9:30 PM, 10:30 PM, 11:30 PM** (Mon–Fri) | Intraday monitor — checks if stop-loss or take-profit targets are hit |
| **2:47 AM** (Tue–Sat) | End of day — reviews overnight thesis, closes weak positions, sends email report |
| **4:23 AM** (Saturdays) | Weekly summary — full week performance review, email sent |

---

## The 5 Rules Before Any Trade

All 5 must be true at the same time. If any one fails, no trade is placed.

### Rule 1 — Research Score ≥ 70/100
The bot asks Perplexity AI to analyze each stock across 6 dimensions:
- Recent news and catalysts (last 48 hours)
- Analyst upgrades/downgrades and price targets
- Volume vs 30-day average
- Price vs 50-day and 200-day moving averages
- RSI (momentum indicator)
- Sector momentum

A score below 70 means the signal is too weak to risk money.

### Rule 2 — Volume ≥ 1.25x Normal
The stock must be trading at least 25% above its normal daily volume. This confirms that above-average institutional interest is present. The threshold was lowered from 2x to 1.25x because the bot's data source (Alpaca IEX feed) captures only a fraction of total market volume, making 2x too strict in practice.

### Rule 3 — SPY Above Its 5-Day Average
The overall market must be in an uptrend. If the whole market is falling, even good stocks tend to fall with it. The bot waits for market health before entering.

**Exception:** When SPY is BELOW the 5-day average, the bot switches to evaluating SH (inverse ETF) instead of regular stocks.

### Rule 4 — VIX Below 28
Fear must be low enough to trade. When VIX is above 28, markets are volatile and unpredictable — stops get hit randomly, even correct trades lose money. The bot sits in cash.

### Rule 5 — No Existing Halt
- Daily portfolio loss must be below 2%
- Daily trade count must be below 3

---

## Position Sizing

The bot never risks more than **5% of total portfolio per trade**.

| Portfolio Value | Max Per Trade |
|---|---|
| $100,000 | $5,000 |
| $50,000 | $2,500 |
| $10,000 | $500 |

For SH (inverse ETF): max is **3% of portfolio** — smaller because inverse ETFs can reverse quickly.

---

## Exit Rules

### Stop-Loss (cut losses)
| Stock Type | Stop-Loss Level |
|---|---|
| Regular stocks | 5% below entry price |
| High-beta stocks (volatile, beta > 1.5) | 7% below entry price |
| SH (inverse ETF) | 5% below entry price |

### Take-Profit (lock in gains)
| Level | Gain | Action |
|---|---|---|
| Tier 1 | +8% | Sell 33% of position |
| Tier 2 | +15% | Sell another 33% |
| Tier 3 | +25% | Sell final 34% |

These three tiers are recorded as the plan at entry time, but the intraday monitor currently enforces exits through two mechanisms instead of firing three separate partial sells:

1. **Broker-side stop-limit order** — placed automatically the moment a trade opens, at the stop-loss price. This protects the position even if the bot is offline, since Alpaca holds the order, not the bot.
2. **Trailing stop after Target 1** — once the price reaches +8% (Target 1), the bot starts tracking the intraday high. If price then pulls back 3% from that high, the *entire remaining position* is closed (not just a partial sell). This is the trailing-stop mechanism, separate from the fixed 5%/7% stop-loss above.

In practice this means a winning trade is far more likely to exit in one shot via the trailing stop than to be sold off in three discrete 33% chunks at each tier.

### Force-Close Triggers (sell immediately regardless of P&L)
- Perplexity AI detects a major negative news reversal for the stock
- VIX spikes above 30 during the day
- End of day and no strong reason to hold overnight (confirmed by Perplexity)
- SPY reclaims its 5-day MA while holding SH (inverse ETF thesis is resolved)

---

## Inverse ETF Mode (SH)

When the market is in a short-term pullback (SPY below 5-day MA), the bot switches into inverse ETF mode:

- **What it buys:** SH — a fund that goes up when SPY goes down
- **Entry threshold:** Score ≥ 60 (lower than the 70 required for stocks)
- **Position size:** 3% of portfolio max (vs 5% for stocks)
- **Exit trigger:** As soon as SPY recovers above its 5-day MA, SH is sold — the thesis is gone
- **Why only SH:** SH is 1x (not leveraged). Leveraged inverse ETFs (SQQQ, SPXS) are too risky

---

## Hard Rules (Cannot Be Changed Without Code)

These are enforced in the code — they cannot be overridden by editing memory files:

| Rule | Value |
|---|---|
| Max position size | 5% of portfolio (3% for SH) |
| Daily loss halt | -2% triggers full stop for the day |
| Max trades per day | 3 |
| No options | Only stocks and approved ETFs |
| Paper trading | Until `live_trading: true` is set in strategy.md |

---

## Memory Files (The Bot's Brain)

All state is stored as text files in the `memory/` folder. You can read and edit these directly.

| File | What It Contains |
|---|---|
| `strategy.md` | Master rules — the bot reads this first every single run |
| `watchlist.md` | Stocks the bot monitors + inverse ETFs |
| `research_cache.md` | Latest scores for each stock (refreshed daily) |
| `daily_context.md` | Today's SPY trend, VIX level, sector leaders |
| `open_positions.md` | All currently held positions with entry, stop, and targets |
| `trade_log.md` | Complete history of every trade ever made |
| `portfolio_state.md` | Current cash, equity, and daily P&L |
| `weekly_trade_counter.md` | Despite the name, this tracks *today's* trade count and the daily loss halt flag — it's reset to 0 every day at EOD, not weekly |
| `trade_trigger.md` | Manual/on-demand trade request. Set `status: pending` and the bot picks it up and runs a market-open evaluation immediately, then updates status to `executing` → `done` (or `error` with details) |
| `benchmark_tracking.md` | Daily portfolio vs SPY performance comparison |
| `performance_metrics.md` | Overall win rate, profit factor, all-time stats |
| `learned_patterns.md` | Weekly reflections on what worked and what didn't |
| `reasoning.md` | Append-only journal of every bot decision |
| `risk_rules.md` | Numerical thresholds (editable to tune the bot) |
| `news_events.md` | Upcoming earnings, Fed meetings, economic calendar |
| `pending_orders.md` | Orders placed but awaiting fill |

---

## Backup & Syncing

Before each routine runs, the bot pulls the latest `memory/` files from GitHub. After any action that changes state (trade opened/closed, halt triggered, counters reset, report sent), it commits and pushes the `memory/` folder back to GitHub automatically. This means:
- Every decision is versioned — you can see the full history in the GitHub commit log
- If you edit a memory file by hand and the bot is about to run, make sure your edit is saved before the scheduled time, or it may be overwritten by the next pull

---

## Tuning the Bot (Without Code)

Edit `memory/risk_rules.md` to adjust thresholds. Changes take effect on the next routine run.

Common adjustments:
- Raise `Min research score` from 70 to 80 → fewer but higher-conviction trades
- Lower `Max VIX` from 28 to 22 → only trade in very calm markets
- Change `SPY must be above N-day MA` from 5 to 10 → require a longer confirmed uptrend

Do NOT edit `memory/strategy.md` hard rules unless you fully understand the consequences.

---

## How to Switch to Live Trading

When you are ready to trade real money:

1. Open `memory/strategy.md`
2. Change `live_trading: false` to `live_trading: true`
3. Make sure your `.env` file has your **live** Alpaca API keys (not paper keys)
4. The bot will automatically use the live account on the next run

**Recommended:** Only do this after at least 4 weeks of paper trading with consistent positive results.

---

## Email Reports

The bot sends emails to `jankla2010@gmail.com` for:
- End-of-day summary (daily P&L, trades, open positions, vs SPY)
- Trade alerts (when a buy or sell is executed)
- Halt alerts (when the -2% daily loss cap is triggered)
- Weekly summary (every Saturday — full week performance)

---

## Current Status

- **Mode:** Paper trading (fake money)
- **Starting balance:** $100,000
- **Trades made:** 6 (NVDA, AMZN, META, NVDA, AAPL, META — all closed same-day, no overnight holds yet)
- **Current equity:** ~$99,648 (as of 2026-07-17 EOD)
- **Open positions:** 0
- **Inverse ETF:** SH added to watchlist — will activate when SPY is below 5-day MA

This section reflects a point-in-time snapshot and will drift out of date — check `memory/portfolio_state.md` and `memory/trade_log.md` for the current numbers.
