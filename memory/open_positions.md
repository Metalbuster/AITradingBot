# Open Positions

Last updated: 2026-07-20 09:39 ET (intraday monitor routine)

| Ticker | Shares | Entry Price | Entry Date | Cost Basis | Stop-Loss | TP1 (+8%) | TP2 (+15%) | TP3 (+25%) | Order ID |
|---|---|---|---|---|---|---|---|---|---|
| META | 7 | $640.637143 | 2026-07-20 (found on Alpaca, not previously recorded — opened by market-open trigger) | $4,484.46 | $608.61 | $691.89 | $736.73 | $800.80 | unknown |

NOTE (2026-07-20 09:39 ET): Intraday check. Same memory/live-account drift as
2026-07-16/17 — open_positions.md said "no open positions" but Alpaca GET
/v2/positions shows META (7sh, avg entry $640.637143) opened by today's 08:37 ET
market-open trigger, never logged here or in trade_log.md. Current price $642.64
(+0.31% vs entry) — no stop-loss or TP trigger. Portfolio equity $99,662.00 vs
last_equity $99,648.12 = +0.014% daily, well within -2% halt threshold. No exits
executed this check. Flagging again: coordinator.py/risk_manager.py/technical.py/
reporter.py/alpaca_client.py all still show uncommitted edits per git status —
likely still the root cause of positions not being written to memory on fill.

## Position History

NOTE (2026-07-17 11:30 ET): Intraday check. AAPL current price $331.85 (-0.59% vs entry) —
no stop-loss or TP trigger. META current price $643.71 (+0.63% vs entry) — no stop-loss
or TP trigger. Portfolio equity $99,613.73 vs last_equity $99,613.15 = +0.0006% daily,
well within -2% halt threshold. No exits executed this check.

NOTE (2026-07-17 10:34 ET): Intraday check. AAPL current price $334.01 (+0.06% vs entry) —
no stop-loss or TP trigger. META current price $630.29 (-1.47% vs entry) — no stop-loss
or TP trigger. Portfolio equity $99,549.04 vs last_equity $99,613.15 = -0.06% daily,
well within -2% halt threshold. No exits executed this check.

NOTE (2026-07-17 09:30 ET): Intraday monitor routine found open_positions.md showing
"no open positions," but Alpaca GET /v2/positions live shows AAPL (14sh) and META (7sh)
currently held — neither was recorded here or in trade_log.md. This is the same
memory/live-account drift previously flagged on 2026-07-16 EOD (engine/coordinator.py,
engine/risk_manager.py, engine/technical.py, utils/alpaca_client.py all show
uncommitted in-progress edits per git status — likely cause). Entry dates and order
IDs are unknown since the fills were never logged. Treated Alpaca as source of truth;
computed stop-loss/TP levels above from avg_entry_price. Both positions checked against
stop-loss/TP1 — neither triggered, no exit required this check. Flagging again for
follow-up: find why the coordinator isn't writing position records on fill.

NOTE (2026-07-16 EOD): Alpaca live account was found holding AMZN, META, and NVDA
at the start of this routine — META and NVDA were never recorded here or in
trade_log.md (likely written outside the normal memory-write path while
engine/coordinator.py etc. were mid-edit; see reasoning.md for detail).
All three were closed EOD per the no-overnight-thesis force-close trigger:
- AMZN: 19sh, exit ~$248.63, close order ba... see trade_log.md
- META: 7sh, exit ~$662.46, close order ba5820ad-a2c6-46a0-b33b-6a72cfa9ba91
- NVDA: 23sh, exit ~$206.36, close order b84d91df-7fd9-4d68-b749-521a52710c65
- AMZN close order b5db3b7c-935e-4535-9a39-3802edc5b718 (its prior GTC stop-limit
  order 6824c992 was cancelled first to free the shares)

NVDA (23 shares) closed EOD via market order at ~$207.88.
Close order ID: 9317f93a-81f0-4727-bdbf-2f04439647be
Reason: Perplexity AI found no strong confirmed overnight catalyst. Strategy force-close trigger applied.

