from typing import List


HOLDINGS_REQUIRED_COLUMNS: List[str] = [
    "PortfolioName",
    "SecName",
    "Qty",
    "PL_DTD",
    "PL_MTD",
    "PL_QTD",
    "PL_YTD"
]



TRADES_REQUIRED_COLUMNS: List[str] = [
    "PortfolioName",
    "TradeTypeName"
]
