import os
from dotenv import load_dotenv

load_dotenv()

# --- API credentials ---
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "jankla2010@gmail.com")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")

# --- Paths ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_DIR = os.path.join(ROOT_DIR, "memory")
LOGS_DIR = os.path.join(ROOT_DIR, "logs")

# --- Hard rules (mirrors strategy.md — code enforcement layer) ---
MAX_POSITION_PCT = 0.05        # 5% of portfolio per trade
DAILY_LOSS_CAP_PCT = 0.02      # -2% daily loss halts all routines
MAX_TRADES_PER_DAY = 3
ALLOW_OPTIONS = False          # stocks only

# --- Soft thresholds (also in risk_rules.md — editable) ---
MIN_RESEARCH_SCORE = 70
MIN_VOLUME_MULTIPLIER = 2.0
MAX_VIX = 28.0
SPY_MA_DAYS = 5
STOP_LOSS_DEFAULT_PCT = 0.05
STOP_LOSS_HIGH_BETA_PCT = 0.07
HIGH_BETA_THRESHOLD = 1.5
TAKE_PROFIT_T1_PCT = 0.08
TAKE_PROFIT_T2_PCT = 0.15
TAKE_PROFIT_T3_PCT = 0.25
TRAILING_STOP_PCT = 0.03

# --- Initial watchlist ---
WATCHLIST_SEEDS = [
    "AAPL", "MSFT", "NVDA", "TSLA", "AMZN",
    "META", "GOOGL", "AMD", "SMCI", "PLTR",
    "SOFI", "RIVN", "COIN", "SPY", "QQQ",
]
