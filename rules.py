def apply_rules(data: dict) -> dict:
    """
    Applies post-parsing enrichment rules.
    Safe against missing keys.
    """

    # -------------------------------------------------
    # LIMIT BUFFER SAFETY
    # (only if parser didn't already create it)
    # -------------------------------------------------
    limit = data.get("limit")

    if limit is not None and "limit_buffer" not in data:
        data["limit_buffer"] = round(limit * 1.10, 2)

    # -------------------------------------------------
    # SENTIMENT CLASSIFICATION
    # -------------------------------------------------
    ticker = data.get("ticker")

    if ticker:
        high_risk = {"SPX", "XSP", "VIX", "NQ", "ES"}

        if ticker in high_risk:
            data["sentiment"] = "RISKY"
        else:
            data["sentiment"] = "MODERATE"

    return data