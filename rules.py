def apply_rules(data: dict) -> dict:
    """
    Applies post-parsing rules safely.
    No KeyError possible.
    """

    # ----- LIMIT BUFFER -----
    limit = data.get("limit")
    if limit is not None:
        data["limit_buffer"] = round(limit * 1.10, 2)

    # ----- SENTIMENT -----
    ticker = data.get("ticker")
    if ticker:
        data["sentiment"] = "RISKY" if ticker == "SPX" else "MODERATE"

    return data