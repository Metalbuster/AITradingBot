# Weekly Trade Counter

Week of: 2026-07-07
trades_this_week: 0
max_trades_per_week: 3
trades_remaining: 3

## Halt Flags
daily_loss_halt: false
halt_reason:
halt_date:

## EOD Reset — 2026-07-04 (Saturday EOD)
daily_loss_halt reset to false by EOD Saturday routine.
trades_this_week reset to 0 for new week (2026-07-07).

## EOD Reset — 2026-07-07 (Tuesday EOD)
daily_loss_halt confirmed/reset to false. trades_this_week confirmed/reset to 0 (was already 0 — no trades placed this week).

## EOD Reset — 2026-07-08 (Thursday EOD)
daily_loss_halt confirmed/reset to false. trades_this_week confirmed/reset to 0 (was already 0 — no trades placed this week).

## EOD Reset — 2026-07-09 (Friday EOD)
daily_loss_halt confirmed/reset to false. trades_this_week confirmed/reset to 0 (was already 0 — no trades placed this week).

## Trade History This Week
| Date | Ticker | Shares | Entry | Order ID |
|---|---|---|---|---|
| (no trades yet) | — | — | — | — |

## EOD Reset — 2026-07-11 (Saturday EOD)
daily_loss_halt confirmed/reset to false. trades_this_week confirmed/reset to 0 (was already 0 — no trades placed this week).

## EOD Reset — 2026-07-14 (Tuesday EOD)
daily_loss_halt set to false. trades_this_week reset to 0 (was already 0 — no trades placed today).

## EOD Reset — 2026-07-15 (Wednesday EOD, closing 2026-07-14 Tuesday session)
daily_loss_halt set to false (was already false). trades_this_week reset to 0 (was already 0 — no trades placed on 2026-07-14).

## EOD Reset — 2026-07-16 (Thursday EOD, closing 2026-07-15 session)
daily_loss_halt set to false (was already false). trades_this_week reset to 0 (was already 0 — no trades placed on 2026-07-15).

- 2026-07-16: BUY AMZN @ $254.25 (counted)

## EOD Reset — 2026-07-16 (Friday-cycle EOD, closing Thursday 2026-07-16 session)
daily_loss_halt set to false (was already false; daily loss -0.26%, well within -2% cap).
trades_this_week reset to 0/3 (was 1/3 — AMZN entry counted for the week is now cleared
per scheduled EOD reset instructions; note AMZN, META, and NVDA were all force-closed
EOD today with no overnight thesis — see reasoning.md and trade_log.md).

## EOD Reset — 2026-07-17 (Saturday-cycle EOD, closing Friday 2026-07-17 session)
daily_loss_halt set to false (was already false; daily gain +0.04%, well within -2% cap).
trades_this_week reset to 0/3 (AAPL and META were both force-closed EOD today with no
overnight thesis — see reasoning.md and trade_log.md; these were exits of an entry
made earlier in the day, per the market-open routine trigger).

- 2026-07-20: BUY AAPL @ $326.77 (counted)

## EOD Reset — 2026-07-20 (Tuesday EOD)
daily_loss_halt set to false (was already false; daily gain +0.03%, well within -2% cap).
trades_this_week reset to 0/3 (was 1/3 — AAPL entry counted for the week is now cleared
per scheduled EOD reset instructions; AAPL, AMZN, and META were all force-closed EOD
today with no overnight thesis — see reasoning.md and trade_log.md).

## EOD Reset — 2026-07-21 (Wednesday EOD)
daily_loss_halt set to false (was already false; daily change -0.00%, well within -2% cap).
trades_this_week reset to 0/3 (was already 0/3 — META was a carried-over position from a
prior undated entry, not a new trade counted this week; force-closed EOD today with no
overnight thesis — see reasoning.md and trade_log.md).
