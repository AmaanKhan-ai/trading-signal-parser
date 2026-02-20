import re
from utils import get_time_cst


def parse_trade(text: str) -> dict:
    data = {}

    msg = text.lower()

    # -------------------------------------------------
    # HELPER (safe word matching)
    # -------------------------------------------------
    def contains_word(words, message):
        return any(re.search(rf"\b{w}\b", message) for w in words)

    # -------------------------------------------------
    # ACTION (expanded vocabulary + typo tolerance)
    # -------------------------------------------------
    buy_words = [
        "buy", "bought", "bougth", "bot",
        "adding", "add", "entered",
        "entry", "longed"
    ]

    sell_words = [
        "sell", "sold", "sodl", "seld",
        "trim", "trimmed", "scaling",
        "scaled", "exit", "closing", "closed"
    ]

    cover_words = ["cover", "covered", "covering"]

    if contains_word(buy_words, msg):
        data["action"] = "BUY"

    elif contains_word(sell_words, msg):
        data["action"] = "SELL"

    elif contains_word(cover_words, msg):
        data["action"] = "COVER"

    # -------------------------------------------------
    # POSITION
    # -------------------------------------------------
    if re.search(r"\blong\b", msg):
        data["position"] = "LONG"
    elif re.search(r"\bshort\b", msg):
        data["position"] = "SHORT"

    # -------------------------------------------------
    # OPTION (strike + type)
    # Supports: 5200C, 5200 C, 5200c
    # -------------------------------------------------
    option_match = re.search(r"(\d{3,5})\s*([cCpP])\b", text)

    if option_match:
        data["strike"] = int(option_match.group(1))
        data["type"] = (
            "CALL" if option_match.group(2).upper() == "C" else "PUT"
        )

    # -------------------------------------------------
    # TICKER (SMART PRIORITY DETECTION)
    # -------------------------------------------------

    KNOWN_TICKERS = {
        "SPX", "SPY", "ES", "NQ", "QQQ", "IWM",
        "NVDA", "TSLA", "AAPL", "AMD", "META",
        "MSFT", "AMZN", "NFLX", "GLD", "SLV",
        "XSP", "VIX"
    }

    words = re.findall(r"\b[A-Z]{1,6}\b", text)

    # Step 1 — known tickers first
    for word in words:
        if word in KNOWN_TICKERS:
            data["ticker"] = word
            break

    # Step 2 — ticker near option
    if "ticker" not in data:
        ticker_match = re.search(
            r"\b([A-Z]{1,6})\s*\d{3,5}\s*[cCpP]\b",
            text
        )
        if ticker_match:
            data["ticker"] = ticker_match.group(1)

    # Step 3 — fallback detection
    if "ticker" not in data:
        ignore_words = {
            "BUY", "SELL", "LONG", "SHORT",
            "CALL", "PUT", "TP", "LOTTO",
            "RUNNER", "HOLD", "OTHER", "APP",
            "HERE", "EXP", "INFRA", "TRADE",
            "ALERT", "ROLE"
        }

        for t in words:
            if t not in ignore_words:
                data["ticker"] = t
                break

    if "ticker" in data:
        data["ticker"] = data["ticker"].upper()

    # -------------------------------------------------
    # LIMIT PRICE (supports .85 , 4. , 5,)
    # -------------------------------------------------
    limit_match = re.search(r"\bat\s+(\d*\.?\d+)[,]?", msg)

    if limit_match:
        limit = float(limit_match.group(1))
        data["limit"] = limit
        data["limit_buffer"] = round(limit * 1.10, 2)

    # -------------------------------------------------
    # EXPIRY DATE
    # -------------------------------------------------
    expiry_match = re.search(
        r"exp[:\s]+(\d{2}/\d{2}/\d{4})",
        msg
    )

    if expiry_match:
        data["expiry"] = expiry_match.group(1)

    # -------------------------------------------------
    # QUANTITY
    # -------------------------------------------------
    percent_match = re.search(r"(\d+)%", msg)

    if percent_match:
        data["quantity"] = f"{percent_match.group(1)}%"
    else:
        quantity_patterns = [
            r"all except \d+ runners?",
            r"last \d+ runners?",
            r"holding \d+",
            r"sold most",
            r"most",
            r"rest"
        ]

        for pattern in quantity_patterns:
            q = re.search(pattern, msg)
            if q:
                data["quantity"] = q.group(0)
                break

    # -------------------------------------------------
    # CONTEXT TAGS
    # -------------------------------------------------
    context_words = [
        "risky",
        "lotto",
        "cheap lotto",
        "runner",
        "tp",
        "roll",
        "third roll",
        "hold",
        "holding",
        "quick trade",
        "keep it small"
    ]

    context = []
    for word in context_words:
        if word in msg:
            context.append(word.title())

    # remove duplicates safelys
    context = list(dict.fromkeys(context))

    if context:
        data["context"] = " ".join(context)

    # -------------------------------------------------
    # TIME (single source — ALWAYS included)
    # -------------------------------------------------
    data["time"] = get_time_cst()

    return data