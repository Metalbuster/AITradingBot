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
