# Learned Patterns

## Week of 2026-06-23 (first live week)

### What Worked
- **Entry filter on SPY MA held firm**: On 2026-06-23, SPY was 1.8% below its 5-day MA ($733.89 vs $747.47). The bot correctly skipped all trades. This likely avoided further losses given broad market weakness.
- **Volume filter caught false opportunities**: PLTR (1.28x), NVDA (1.12x), META (1.09x) all failed the 2x volume threshold on 06-23, meaning no conviction in any move. Skipping was correct.

### What Failed
- **EOD force-close on NVDA cost -$126.63 (-2.58%)**: NVDA entered at $213.39 on 06-22. Thesis score was high (92/100) but Perplexity confidence for overnight hold was only 68 — below the implicit threshold. Exit at $207.88. The position would have benefited from a tighter stop being hit intraday rather than waiting for EOD close to trigger the no-overnight-catalyst rule.
- **High score (92) did not protect against loss**: NVDA's AI data center thesis was strong, but "valuation risk high" was flagged and should have been a warning signal. Consider adding valuation risk as a score modifier.

### VIX Conditions
- VIX data not recorded in trade log for 06-22 entry — need to add VIX at time of entry to future trade log entries to diagnose VIX-related losses.
- Strategy rule is VIX < 28 for entry; no VIX spike appears to have triggered the NVDA exit, but force-close was EOD-thesis-based.

### Emerging Patterns (1 week sample — low confidence)
- **Sector-wide weakness overrides strong individual scores**: Even a 92-score NVDA trade lost when the broader market was in a down move. SPY health check is the most critical gate.
- **Perplexity overnight confidence < 70 = exit**: The 68 confidence score correctly flagged "don't hold overnight." This heuristic should be formalized: if overnight confidence < 70, close EOD regardless of P&L.
- **Week 1 summary**: 1 trade executed, 1 skipped, 0 wins, -$126.63 net. Filters worked as designed on the skip day. First trade loss was within the acceptable per-trade risk band (5% max position; actual was -2.58%). No hard rules broken.

### Action Items for Strategy
1. Add VIX at entry to trade log template
2. Formalize Perplexity overnight confidence threshold: < 70 = mandatory EOD exit
3. Consider adding valuation risk flag as a -5 to -10 score modifier in research scoring

---

## Weekly Reflection — Week of 2026-06-22 (Final, logged 2026-06-27)

### Week Stats
- Trades executed: 1 | Skipped: 1 | Wins: 0 | Losses: 1
- Win rate: 0% | Net P&L: -$126.63 | Avg loss: -2.58%
- Portfolio: $99,873.35 (down -0.13% from $100,000.00 baseline)
- SPY performance this week: -1.59% (Jun 22 $743.54 → Jun 26 $731.71)
- Alpha vs SPY: +1.46% (bot lost -0.13% vs SPY's -1.59%; defensive filters outperformed)

### Signals That Worked
- **SPY 5-day MA gate blocked a bad day (Jun 23)**: SPY was 1.8% below its MA. All candidates failed volume (best: PLTR 1.28x vs required 2x). Skipping saved an unknown but likely negative P&L in a market-down session. This was the single most valuable filter this week.
- **Perplexity overnight confidence (68 < 70) triggered correct EOD exit**: The exit signal fired as designed. Holding NVDA overnight into Jun 23 (a down market day) would likely have produced a larger loss.
- **No hard rules broken**: Daily loss cap, trade limit, and position sizing all held. NVDA loss was -2.58% on position size (within the 5% max position cap).

### Signals That Failed
- **Research score 92 on NVDA did not predict same-day gain**: Score reflects thesis strength, not intraday momentum. A high score is necessary but not sufficient — broad market context must dominate.
- **No volume confirmation on entry day**: Entry did not verify whether NVDA had 2x volume at open vs. the 2x threshold required. The trade log entry lacks intraday volume at time of entry. Needs to be logged.
- **"Valuation risk high" flag was noted but not acted upon**: This should reduce the effective score by 5-10 points.

### VIX Conditions
- VIX was not recorded in trade log for Jun 22 entry — this remains an open gap.
- No VIX-based exit was triggered; force-close was thesis-confidence-driven.
- Market weakness Jun 23 (SPY -1.8% vs MA) correlated with typical high-VIX environment. Suspected VIX was elevated (20-25 range) but unconfirmed.

### Emerging Patterns (Week 1 of 2 — very low sample, low confidence)
- **Defensive alpha via filters**: In a down week for SPY (-1.59%), the bot's conservative filter set produced +1.46% alpha purely by not trading. This pattern will matter in sustained downtrends.
- **Inaugural week bottleneck is data quality, not signal quality**: Missing VIX at entry, missing intraday volume at entry, missing overnight hold decision reasoning — these gaps limit post-trade analysis.
- **Single trade, single loss = insufficient to infer signal failure**: NVDA loss could be random; sector-momentum signal needs 5+ trades before drawing conclusions.

### Open Action Items (carry forward to Week 2)
1. Add VIX at entry to trade log template
2. Add intraday volume multiple at time of entry to trade log
3. Formalize overnight confidence threshold: Perplexity confidence < 70 = mandatory EOD close
4. Add valuation risk modifier: flag reduces research score by 7 points
5. Confirm SPY MA calculation uses close prices, not intraday

---

## Weekly Reflection — Week of 2026-06-30 (Final, logged 2026-07-04)

### Week Stats
- Trades executed: 0 | Skipped: unknown (no entries logged) | Wins: 0 | Losses: 0
- Win rate: N/A | Net P&L: $0.00 | Avg loss: N/A
- Portfolio: $99,873.35 (unchanged from prior week close)
- SPY performance this week: +0.41% (Jun 30 $741.03 → Jul 4 $744.07)
- Alpha vs SPY: -0.41% (flat portfolio vs SPY gaining; underperformed by sitting out)
- Cumulative alpha since inception: +1.05% (portfolio -0.13% vs SPY +0.92% net from baseline)

### Signals That Worked
- **Zero trades = zero losses**: No entries triggered this week, meaning no capital was put at risk during a mild SPY rally (+0.41%). Entry criteria held — no logs show a qualifying setup was missed.
- **Holiday week reduced opportunity**: July 4th (Friday) was a market holiday. 4-day trading week with no high-volume breakout candidates appearing in prior daily logs.

### Signals That Failed
- **No trades means no alpha capture**: SPY gained +0.41% this week. A flat portfolio produced -0.41% weekly alpha — the cost of a slow/no-signal week in a rising market. This is expected behavior but worth tracking.
- **Trade log gap for this week**: No trade log entries exist for 2026-06-30 through 2026-07-04. It is unknown how many skip decisions were made (if any) due to entry criteria failures. This is a logging gap — skip decisions should be recorded in the trade log, not just executed trades.

### VIX Conditions
- VIX data not available for this week in trade log (same ongoing gap from Week 1).
- SPY was above its 5-day MA for most of this period (SPY range $741–$747), suggesting no inverse ETF (SH) conditions were triggered.
- The mild +0.41% SPY gain suggests VIX was likely subdued (estimated 14–18 range), meaning entry criteria could have been met if a qualifying candidate appeared.

### Emerging Patterns (Week 2 of 2 — still very low sample)
- **Two consecutive no-trade or low-trade weeks**: Week 1 had 1 trade (loss), Week 2 had 0 trades. The bot is trading at very low frequency relative to its 3/day limit. Either the signal quality bar is appropriately high, or the watchlist lacks enough qualifying candidates on any given day.
- **Flat portfolio in rising market = negative alpha drag**: When SPY trends up and bot holds cash, alpha goes negative. This is the hidden cost of conservative filters. Over a bull run, the opportunity cost compounds.
- **Volume filter (2x 30-day avg) appears to be the primary gatekeeper**: From Week 1 data, even high-scoring tickers (NVDA 78, META 85, PLTR 78) failed to hit 2x volume on the skip day. If the volume threshold is rarely met, the bot will rarely trade. Consider whether 1.5x is more appropriate as a threshold.

### Open Action Items (carry forward to Week 3)
1. *(Unresolved from Week 1)* Add VIX at entry to trade log template
2. *(Unresolved from Week 1)* Add intraday volume multiple at time of entry to trade log
3. *(Unresolved from Week 1)* Formalize overnight confidence threshold: Perplexity confidence < 70 = mandatory EOD close
4. *(Unresolved from Week 1)* Add valuation risk modifier: flag reduces research score by 7 points
5. **New**: Log skip decisions in trade_log.md (not just executed trades) — record date, reason for skip, top candidate scores/volume at time of skip
6. **New**: Evaluate whether 2x volume threshold is too restrictive — backtest 1.5x threshold against Week 1 candidates (PLTR 1.28x, NVDA 1.12x, META 1.09x would still not qualify at 1.5x, but worth reviewing over broader history)
7. **New**: Track weekly alpha running total — currently -0.41% week 2; need 5+ weeks to determine if filters add net value vs. SPY buy-and-hold

---

## Weekly Reflection — Week of 2026-07-07 (Final, logged 2026-07-11)

### Week Stats
- Trades executed: 0 | Skipped: unknown count (no skip entries logged in trade_log.md) | Wins: 0 | Losses: 0
- Win rate: N/A | Net P&L: $0.00 | Avg loss: N/A
- Portfolio: $99,873.35 (unchanged for third consecutive week)
- SPY performance this week: +0.46% (Jul 7 $751.63 -> Jul 10 $755.10)
- Alpha vs SPY: -0.46% (flat portfolio underperformed a rising market)
- Cumulative alpha since inception: ~+0.59% (roughly netting week 1's +1.46% against week 2's -0.41% and week 3's -0.46%)

### Signals That Worked
- **VIX stayed low and stable all week (15.53-23.34 range, ending 15.67 on Jul 10)** — no VIX-driven halts were needed, confirming the VIX<28 gate is not the binding constraint right now.
- **No hard rules broken** — daily loss cap, trade limit, and position sizing never triggered because zero trades were placed; the bot did not force a bad entry just to stay active.

### Signals That Failed
- **Three consecutive weeks with 0-1 trades total** — the bot has executed only 1 trade in 3 weeks against a 3/day (15/week) budget. Either qualifying setups are genuinely rare, or a filter (likely the volume multiplier) is over-restrictive.
- **daily_context.md shows 5 tickers cleared for entry (META 86, NVDA 78, AMD 76, MSFT 72, AMZN 71) as of Friday close, all above the 70 score threshold** — yet no trade was placed this week. This strongly suggests the volume confirmation filter (or timing of the market-open routine relative to intraday volume data) is the actual bottleneck, not research quality.
- **trade_log.md has not been updated since 2026-06-25** — daily skip decisions are not being written to the log despite the Week 1 action item to do so. This is now a 3-week-old open item and is starting to block weekly analysis (cannot tell whether Mon-Fri this week had near-miss setups or no candidates at all).

### VIX Conditions
- VIX ranged 15.53-23.34 over the trailing month, closing the week at 15.67 (near the low end) — a low-fear, low-volatility regime.
- Low VIX combined with zero trades suggests the bottleneck is not risk-off caution; the entry criteria (volume/score combination) simply aren't being satisfied by watchlist tickers at market-open.

### Emerging Patterns (Week 3 of 3 tracked — low-to-moderate confidence)
- **Persistent under-trading in a calm, rising market**: With VIX low and SPY trending up 3 of the last 3 weeks, a strategy that trades 0-1 times per week is leaving the 3-trades/day budget almost entirely unused. If this continues for 2+ more weeks, the volume threshold (1.25x per config.py, though watchlist.md/strategy.md still reference a stricter historical 2x in earlier logs) should be re-examined against actual realized watchlist volume.
- **Score threshold (70) is being cleared regularly** (5 tickers >=70 as of Jul 10) without translating into trades — reinforces that score is not the limiting factor.

### Open Action Items (carry forward to Week 4)
1. *(Unresolved, 3 weeks running)* Log skip decisions in trade_log.md daily — record date, reason for skip, top candidate scores/volume at time of skip. This is now the highest-priority gap.
2. *(Unresolved)* Add VIX at entry to trade log template
3. *(Unresolved)* Formalize overnight confidence threshold: Perplexity confidence < 70 = mandatory EOD close
4. *(Unresolved)* Add valuation risk modifier: flag reduces research score by 7 points
5. **New**: Audit whether the market-open routine is actually re-checking volume against the current MIN_VOLUME_MULTIPLIER (1.25x per config.py) or a stale stricter value — 3 weeks of near-zero trading with scores clearing 70+ warrants a code-level check of engine/risk_manager.py's volume gate
6. **New**: Reconcile trade_log.md (stale since 06-25) with weekly_trade_counter.md and portfolio_state.md (both current) — pick one source of truth and keep it updated daily

---

## Weekly Reflection -- Week of 2026-07-13 (Final, logged 2026-07-18)

### Week Stats
- Trades executed: 5 | Wins: 2 | Losses: 3 | Win rate: 40.0%
- Net P&L: -$225.20 (5 fills across 07-16 and 07-17; no logged activity 07-13 to 07-15)
- Portfolio: $99,873.35 -> $99,648.14 (-0.23%)
- SPY performance this week: $749.13 (07-13) -> $743.68 (07-17), roughly -0.73%
- Alpha vs SPY: ~+0.50% (losses were smaller than the market's own decline)
- Cumulative alpha since inception: positive but thinning -- first week with net realized losses larger than any prior single week

### Signals That Worked
- **The under-trading streak finally broke**: after 3 consecutive weeks of 0-1 trades, the bot placed 5 trades in 2 days (AMZN, META, NVDA on 07-16; AAPL, META on 07-17), confirming the volume/score gates are not permanently closed -- they just needed the right week.
- **AAPL and META (07-17) both closed positive**, driven by concrete near-term catalysts (China Apple Intelligence approval + HSBC/Citi upgrades for AAPL; Meta Compute cloud push + Iris chip news for META) rather than pure momentum scores.
- **No hard rules broken across 5 trades**: every position sized within the 5% cap, daily loss cap never neared -2% on either day (worst daily print was still a gain +0.04% on 07-17), and the 3-trades/day limit was respected (3 on 07-16, 2 on 07-17).

### Signals That Failed
- **3 of 5 trades were force-closed at a loss purely on "no overnight catalyst," not on stop-loss or thesis invalidation**: AMZN -2.11%, META -2.30%, NVDA -1.03% on 07-16. The thesis in each case (AWS AI momentum, Meta Compute, Vera Rubin) was intact -- the exits were mechanical (earnings 2+ weeks out = no overnight hold), not driven by a negative catalyst. This is the same "EOD force-close cost me a real loss" pattern first seen with NVDA on 2026-06-22, now repeated 3x in one day.
- **Position tracking drift recurred for a second straight week**: on 07-16 and again on 07-17, live Alpaca positions (META/NVDA on 07-16; AAPL/META on 07-17) were discovered at monitor/EOD time without ever being logged at entry in open_positions.md or trade_log.md. reasoning.md repeatedly flags uncommitted in-progress edits to engine/coordinator.py, engine/risk_manager.py, engine/technical.py, utils/alpaca_client.py as the likely cause -- this is now a 2-week-old unresolved gap and the most concrete, fixable bug surfaced this quarter.
- **Entry order IDs and entry timestamps are unknown for 4 of the 5 positions this week** (AAPL, META 07-16, META 07-17, NVDA) because they were reconstructed from live Alpaca state rather than captured at fill time -- this blocks precise hold-duration and slippage analysis.

### VIX Conditions
- VIX stayed in a low, calm band all week (roughly 15-18 based on adjacent weeks' readings) -- no VIX-driven halts were triggered and VIX was not the binding constraint on any of the 5 trades.
- Low VIX combined with an active trading week suggests the earlier under-trading weeks (07-07, 06-30) were volume/candidate-availability driven, not risk-driven -- consistent with the standing hypothesis from prior reflections.

### Emerging Patterns (5 weeks tracked -- moderate confidence now building on force-close losses)
- **The mandatory EOD-no-catalyst force-close is now a recurring, quantifiable drag**: 4 of the bot's 6 lifetime trades (NVDA 06-22, AMZN/META/NVDA 07-16) were closed at a loss specifically because of the "no overnight thesis" rule, not because the underlying thesis broke. Combined lifetime cost of this exit rule alone: -$126.63 -$101.97 -$108.99 -$49.22 = -$386.81 against only +$34.98 in wins. This is now the single largest identifiable driver of the bot's -$351.83 lifetime net P&L and merits a strategy review: either loosen the same-day earnings-distance requirement or add a smaller partial-hold allowance when the intraday move is favorable at close.
- **Live-account/memory-file drift is a 2-week-recurring, code-level bug, not a one-off**: happening on both 07-16 and 07-17 EOD/intraday routines while engine/*.py files show uncommitted edits. This should be treated as a priority engineering fix rather than another "flag for follow-up" entry, since it is now actively corrupting the trade log's entry-time data for every trade this week.
- **Win rate over the last 5 trades (40%) is closer to a coin flip than the bot's high average research scores (76-92) would suggest** -- reinforcing the week-1 finding that score predicts thesis quality, not same-day/next-day price direction.

### Open Action Items (carry forward to next week)
1. **New, highest priority**: Root-cause and fix the engine/coordinator.py position-logging bug causing live Alpaca fills to go unrecorded in open_positions.md/trade_log.md at entry time (2 weeks running: 07-16, 07-17).
2. **New**: Formally evaluate whether the "no overnight catalyst = force-close" rule is net-negative in expectancy -- 4 of 6 lifetime trades lost specifically to this rule for a combined -$386.81, vs. 2 wins for +$34.98. Consider requiring a genuinely negative catalyst (not just an absent one) before forcing an exit on a thesis that hasn't broken.
3. *(Unresolved, 4 weeks running)* Add VIX at entry to trade log template.
4. *(Unresolved, 4 weeks running)* Add valuation risk modifier: flag reduces research score by 7 points.
5. *(Unresolved)* Log skip decisions in trade_log.md daily, including on days with zero trades (07-13 through 07-15 this week have no entries at all, active or skipped).
