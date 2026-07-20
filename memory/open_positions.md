# Open Positions

Last updated: 2026-07-20 11:50 ET (intraday monitor routine)

| Ticker | Shares | Entry Price | Entry Date | Cost Basis | Stop-Loss | TP1 (+8%) | TP2 (+15%) | TP3 (+25%) | Order ID |
|---|---|---|---|---|---|---|---|---|---|
| AAPL | 15 | $326.77 | 2026-07-20 11:06 ET | $4,901.55 | $310.43 | $352.91 | $375.79 | $408.46 | unknown |
| META | 7 | $640.637143 | 2026-07-20 (found on Alpaca, not previously recorded — opened by market-open trigger) | $4,484.46 | $608.61 | $691.89 | $736.73 | $800.80 | unknown |
| AMZN | 19 | $250.632105 (from Alpaca avg_entry_price, not previously recorded) | unknown | $4,762.01 | $238.10 (computed) | $270.68 (computed) | n/a | n/a | unknown |

NOTE (2026-07-20 11:34 ET): Intraday check. AAPL current price $325.8094
(-0.22% vs memory entry $326.77) — no stop-loss or TP trigger. META current
price $647.955 (+1.14% vs entry) — no stop-loss or TP trigger. AMZN current
price $251.58 (+0.38% vs Alpaca avg entry) — no stop-loss or TP trigger.
Portfolio equity $99,705.51 vs last_equity $99,648.12 = +0.058% daily, well
within -2% halt threshold. No exits executed this check.

NOTE (2026-07-20 11:50 ET): Intraday check. AAPL current price $324.335 (-0.697%
vs Alpaca avg entry $326.61) — no stop-loss ($310.43) or TP trigger. META current
price $651.826 (+1.747% vs entry $640.637143) — no stop-loss or TP trigger. AMZN
current price $252.585 (+0.779% vs entry $250.632105) — no stop-loss or TP trigger.
No SH position held (SPY inverse-ETF logic not applicable). Portfolio equity
$99,730.39 vs last_equity $99,648.12 = +0.0826% daily, well within -2% halt
threshold. No exits executed this check.

DRIFT FLAG (recurring): Alpaca GET /v2/positions shows AMZN (19sh) still open,
but trade_log.md/open_positions.md history says AMZN was force-closed EOD on
2026-07-16. Either that EOD close never executed live, or a new AMZN position
was opened afterward without being logged (same class of drift previously
flagged 2026-07-16/17/20 — coordinator.py/risk_manager.py/technical.py/
reporter.py/alpaca_client.py all still show uncommitted edits per git status,
likely still the root cause of fills not being written to memory). Treating
Alpaca as source of truth; AMZN now tracked above with computed stop/TP1 from
avg_entry_price pending reconciliation.

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



## AAPL — Opened 2026-07-20 11:06 ET
- Entry: $326.77 | Shares: 15 | Cost: $4901.55
- Stop-loss: $310.43 (5% below entry)
- Target 1: $352.91 (+8%) — sell 5 shares
- Target 2: $375.79 (+15%) — sell 5 shares
- Target 3: $408.46 (+25%) — sell 5 shares
- Thesis: Up 22% YTD; briefly overtook NVDA as #1 by market cap ($4.88T); HSBC Hold→Buy PT $260→$366 intact; ATH momentum; earnings July 30 (10 days); RSI elevated post-ATH
- Research score: 73/100
- High-beta: False

