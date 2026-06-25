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
