# Open Positions

Last updated: 2026-07-23 11:30 ET (Intraday monitor check — confirmed flat)

NOTE (2026-07-23 11:30 ET): Intraday check. Alpaca GET /v2/positions confirms
empty — no open positions (matches this file's last EOD state). No SH position
held. Account equity $99,672.34; account.last_equity again returned "0"
(stale/bad field, same recurring anomaly) so daily P&L computed vs last known
EOD equity note ($99,675.82 from 2026-07-21 EOD): -$3.48 (-0.0035%), well
within -2% halt threshold. daily_loss_halt confirmed false in
weekly_trade_counter.md. No exits needed (nothing open). No action taken.

Last updated: 2026-07-23 10:30 ET (Intraday monitor check — confirmed flat)

NOTE (2026-07-23 10:30 ET): Intraday check. Alpaca GET /v2/positions confirms
empty — no open positions (matches this file's last EOD state). No SH position
held. Account equity $99,672.34; account.last_equity again returned "0"
(stale/bad field, same anomaly as 2026-07-22 check — not treated as a real
move) so daily P&L computed vs last known EOD equity note ($99,675.82 from
2026-07-21 EOD): -$3.48 (-0.0035%), well within -2% halt threshold.
daily_loss_halt confirmed false in weekly_trade_counter.md. No exits needed
(nothing open). No action taken.

Last updated: 2026-07-22 09:30 ET (Intraday monitor check — confirmed flat)

NOTE (2026-07-22 09:30 ET): Intraday check. Alpaca GET /v2/positions confirms
empty — no open positions (matches this file's last EOD state). No SH position
held. Account equity $99,672.34; account.last_equity returned "0" (stale/bad
field, balance_asof 2026-07-21 — treated as data anomaly, not a real -100%
move) so daily P&L computed vs last known EOD equity note ($99,675.82 from
2026-07-21 EOD): -$3.48 (-0.0035%), well within -2% halt threshold.
daily_loss_halt confirmed false in weekly_trade_counter.md. No exits needed
(nothing open). No action taken.

Last updated: 2026-07-21 15:57 ET (EOD Wednesday routine — closed to flat)

No open positions. META (7sh) was closed EOD this routine — no strong confirmed
overnight catalyst found (earnings 7/29, 8 days out). Exit $644.25 avg, P&L -$3.46
(-0.08%). Alpaca GET /v2/positions confirmed empty after fill.

## Previously Open (closed this routine)

DRIFT (recurring): Alpaca GET /v2/positions shows META (7sh) still open, despite
open_positions.md/trade_log.md recording it as force-closed EOD on 2026-07-20
(exit price $646.102857, P&L +$38.26). Either that EOD close never executed live,
or a new META position was opened afterward without being logged (same class of
drift previously flagged 2026-07-16/17/20 — coordinator.py/risk_manager.py/
technical.py/reporter.py/alpaca_client.py all still show uncommitted edits per
git status, likely still the root cause). Treating Alpaca as source of truth;
META tracked below with stop/TP computed from Alpaca avg_entry_price, pending
reconciliation.

| Ticker | Shares | Entry Price | Entry Date | Cost Basis | Stop-Loss | TP1 (+8%) | TP2 (+15%) | TP3 (+25%) | Order ID |
|---|---|---|---|---|---|---|---|---|---|
| META | 7 | $644.744285 (Alpaca avg) | unknown | $4513.21 | $612.51 | $696.32 | $741.46 | $805.93 | unknown |

NOTE (2026-07-21 11:30 ET): Intraday check. META current price $648.025 (Alpaca
current_price; latest bar close $647.995) — (+0.509% vs Alpaca avg entry
$644.744285) — no stop-loss ($612.51) or TP trigger. No SH position held (SPY
inverse-ETF logic not applicable — no SH in Alpaca positions). Portfolio equity
$99,698.79 vs last_equity $99,675.82 = +0.023% daily, well within -2% halt
threshold. daily_loss_halt confirmed false in weekly_trade_counter.md. No exits
executed this check.

NOTE (2026-07-21 10:30 ET): Intraday check. META current price $648.03 (+0.509%
vs Alpaca avg entry $644.744285) — no stop-loss ($612.51) or TP trigger. No SH
position held (SPY inverse-ETF logic not applicable — no SH in Alpaca positions).
Portfolio equity $99,698.82 vs last_equity $99,675.82 = +0.023% daily, well within
-2% halt threshold. daily_loss_halt confirmed false in weekly_trade_counter.md.
No exits executed this check.

NOTE (2026-07-21 09:30 ET): Intraday check. META current price $647.215 (+0.383%
vs Alpaca avg entry $644.744285) — no stop-loss ($612.51) or TP trigger. No SH
position held (SPY inverse-ETF logic not applicable — no SH in Alpaca positions).
Portfolio equity $99,693.92 vs last_equity $99,675.82 = +0.018% daily, well within
-2% halt threshold. daily_loss_halt confirmed false in weekly_trade_counter.md.
No exits executed this check.

NOTE (2026-07-20 15:57 ET): EOD Tuesday routine. Perplexity checked for a strong
confirmed overnight catalyst on all three open positions — none found for any
(AAPL earnings 7/30, AMZN earnings 7/30, META earnings 7/29, all 9-10 days out;
no new regulatory/M&A/guidance news in the last 24h). Force-close trigger applied
to all three: AAPL sold 15sh @ $326.746 (P&L -$0.36), AMZN sold 19sh @ $249.97
(P&L -$12.58), META sold 7sh @ $646.102857 (P&L +$38.26). AAPL's close initially
failed with 403 Forbidden because its GTC stop-limit order ($310.43 stop) was
still open and holding the shares — cancelled that order first, then the
sell-to-close succeeded. Alpaca GET /v2/positions confirmed empty after fills.
Account equity $99,675.84 vs last_equity $99,648.12 = +$27.72 (+0.028%), well
within -2% halt threshold.

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

