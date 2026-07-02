Run the trading bot order placement agent. Follow these steps in strict order — do not skip any step.

STEP 1 — Read strategy.md
Read memory/strategy.md. Note the live_trading flag (true = live account, false = paper account).
If the file cannot be read, abort immediately and report the error.

STEP 2 — Check daily trade limit
Read memory/weekly_trade_counter.md.
If trades_this_week >= 3: log "Daily trade limit reached (3/3). No new entries.", call /journal with this message, stop.

STEP 3 — Check daily halt flag
Read memory/weekly_trade_counter.md.
If daily_loss_halt = true: log "Daily loss halt is active. No trades today.", call /journal, stop.

STEP 4 — Load research candidates
Read memory/research_cache.md. Extract all tickers with Score >= 70/100, sorted highest first.
If no candidates meet the threshold: log "No candidates above threshold today.", call /journal, stop.

STEP 5 — Check existing positions (memory)
Read memory/open_positions.md. Note which tickers are already held.

STEP 6 — Verify live positions via Alpaca API (source of truth)
Call Alpaca API: GET /v2/positions
Cross-reference with memory. Remove any candidate already held in either source.

STEP 7 — Get real-time account data
Call Alpaca API: GET /v2/account
Extract: equity (portfolio value), buying_power, cash.
Calculate max_position_dollars = equity × 0.05 (5% hard rule — never exceed this).

STEP 8 — Confirm market context
Read memory/daily_context.md.

If SPY is ABOVE 5-day MA and VIX < 28:
  - Proceed with regular stock candidates (score >= 70). Skip SH.

If SPY is BELOW 5-day MA and VIX < 28:
  - Block all regular stock entries.
  - Check if SH is in the research_cache.md with score >= 60.
  - If yes: proceed with SH only. Max position = equity × 0.03 (3% rule for inverse ETFs).
  - If no: log "SPY below MA, SH not scored or below threshold. No trades today.", call /journal, stop.

If VIX >= 28: log reason, call /journal, stop regardless of SPY direction.

STEP 9 — Evaluate each candidate
For each candidate (highest score first):
  a. Get technical data via Alpaca market data API (latest bar, 30-day volume avg, RSI, MA50)
  b. Confirm volume >= 1.25x 30-day average
  c. Confirm asset_class = us_equity (reject anything else — no options, no crypto)
  d. Calculate shares = floor(max_position_dollars / current_price), minimum 1
  e. If all checks pass: proceed to STEP 10
  f. If checks fail: log reason, move to next candidate

STEP 10 — Place order
Place a LIMIT order at current ask price via Alpaca API.
Order params: symbol, qty=shares, side=buy, type=limit, time_in_force=day.
Immediately after fill confirmation: place a stop-limit order for the full position as stop-loss.

STEP 11 — Update memory files
Update memory/open_positions.md — add new position block with entry price, stop, targets, thesis.
Update memory/trade_log.md — append new row.
Update memory/weekly_trade_counter.md — increment trades_this_week by 1.

STEP 12 — Journal and push
Call /journal with full decision: ticker, score, thesis, entry price, stop price, position size, reason chosen over others.
Commit and push memory/ to GitHub with message: `auto: BUY [TICKER] [N]sh @ $[PRICE] | score:[X] | [date] ET`

After placing one trade: re-check weekly_trade_counter.md. If trades_this_week >= 3, stop evaluating further candidates for today.

SPECIAL EXIT RULE FOR SH:
During intraday monitor, if SH is held and SPY has reclaimed its 5-day moving average (current SPY price > 5-day MA), close SH immediately via market sell order regardless of current P&L. Log reason: "SPY reclaimed 5-day MA — inverse ETF thesis resolved."
