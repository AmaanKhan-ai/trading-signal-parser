import re
from utils import get_time_cst


def parse_trade(text: str) -> dict:
    data = {}
    msg = text.lower()

    # ---------- ACTION ----------
    if "bought" in msg or "buy" in msg:
        data["action"] = "BUY"
    elif "sold" in msg or "selling" in msg:
        data["action"] = "SELL"
    elif "covered" in msg:
        data["action"] = "COVER"

    # ---------- TICKER ----------
    ticker_match = re.search(r"\b(SPX|ES)\b", text)
    if ticker_match:
        data["ticker"] = ticker_match.group(1)

    # ---------- POSITION ----------
    if "long" in msg:
        data["position"] = "LONG"
    elif "short" in msg:
        data["position"] = "SHORT"

    # ---------- OPTION ----------
    option_match = re.search(r"(\d{3,5})(C|P)\b", text)
    if option_match:
        data["strike"] = int(option_match.group(1))
        data["type"] = "CALL" if option_match.group(2) == "C" else "PUT"

    # ---------- LIMIT ----------
    limit_match = re.search(r"\bat\s+(\d+\.?\d*)", msg)
    if limit_match:
        limit = float(limit_match.group(1))
        data["limit"] = limit
        data["limit_buffer"] = round(limit * 1.10, 2)

    # ---------- QUANTITY ----------
    percent_match = re.search(r"(\d+)%", msg)
    if percent_match:
        data["quantity"] = f"{percent_match.group(1)}%"
    else:
        runner_match = re.search(r"(except\s+\d+\s+runner|last\s+\d+|most)", msg)
        if runner_match:
            data["quantity"] = runner_match.group(1)

    # ---------- CONTEXT ----------
    context = []
    for word in ["risky", "lotto", "runner", "tp", "roll", "hold"]:
        if word in msg:
            context.append(word.capitalize())

    if context:
        data["context"] = " ".join(context)

    # ---------- TIME (always) ----------
    data["time"] = get_time_cst()

    return data