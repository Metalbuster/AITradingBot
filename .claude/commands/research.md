Run the trading bot research agent.

Steps (execute in order):
1. Read memory/strategy.md — confirm paper/live mode and that no halt flag is active
2. Read memory/watchlist.md — extract the Active ticker list
3. If arguments were passed to this command (e.g. `/research NVDA TSLA`), research only those tickers instead of the full watchlist
4. For each ticker, call the Perplexity AI API with this structured prompt:
   - Recent news and catalysts (last 48 hours)
   - Analyst sentiment and upgrades/downgrades
   - Volume vs 30-day average (minimum threshold for entry is 1.25x — score volume accordingly)
   - Price vs 50-day and 200-day moving average
   - RSI level
   - Sector momentum
   Score each dimension and produce a total score out of 100. End with: `SCORE: [X]/100`
5. Also query Perplexity for overall market context: SPY trend, VIX level, top sector, macro events in next 48h. End with: `TRADE_OK: yes` or `TRADE_OK: no`
6. Write all results to memory/research_cache.md (overwrite today's entries, preserve format)
7. Write market context to memory/daily_context.md
8. Call /journal with: "Research complete. [N] tickers scanned. Top candidates: [ticker(score), ...]. Market TRADE_OK=[yes/no], VIX=[X]."
9. Commit and push memory/ to GitHub with message: `auto: research update | [N] tickers | [date] [time] ET`

For regular stocks: score each on news, analyst sentiment, volume, technicals, sector momentum. End with SCORE: [X]/100.

For SH (inverse ETF): score it differently — higher score when SPY is falling, VIX is rising, and bearish momentum is confirmed. Ask Perplexity: "Is the S&P 500 in a confirmed short-term downtrend based on the last 5 days?" If yes, SH scores higher. End with SCORE: [X]/100. Minimum threshold for SH is 60 (not 70).

Do not score leveraged inverse ETFs (SQQQ, SPXS, etc.) — SH only.
