from typing import Dict, List

import pandas as pd

from data.loader import DataLoader


class RetrievalError(Exception):
    
    pass


class FundNotFoundError(RetrievalError):
    pass


class RetrievalEngine:
    """
    Executes deterministic queries on holdings and trades data.

    This class must remain:
    - Stateless
    - Predictable
    - Fully testable
    """

    def __init__(self, data_loader: DataLoader):
        self._holdings_df = data_loader.holdings
        self._trades_df = data_loader.trades



    def count_holdings(self, fund_name: str) -> int:
        """
        Count number of holdings for a given fund.
        """
        df = self._filter_by_fund(self._holdings_df, fund_name)
        return len(df)

    def count_trades(self, fund_name: str) -> int:
        """
        Count number of trades for a given fund.
        """
        df = self._filter_by_fund(self._trades_df, fund_name)
        return len(df)



    def aggregate_pl_ytd(self, fund_name: str) -> float:
        """
        Aggregate YTD P&L for a given fund using holdings data.
        """
        df = self._filter_by_fund(self._holdings_df, fund_name)
        return float(df["PL_YTD"].sum())



    def best_performing_fund_ytd(self) -> Dict[str, float]:
        """
        Identify the best performing fund based on YTD P&L.
        """
        grouped = (
            self._holdings_df
            .groupby("PortfolioName", as_index=False)["PL_YTD"]
            .sum()
        )

        if grouped.empty:
            raise RetrievalError("No holdings data available for comparison.")

        best_row = grouped.loc[grouped["PL_YTD"].idxmax()]

        return {
            "fund": best_row["PortfolioName"],
            "pl_ytd": float(best_row["PL_YTD"])
        }



    def _filter_by_fund(self, df: pd.DataFrame, fund_name: str) -> pd.DataFrame:
        """
        Filter dataframe by fund name with strict validation.
        """
        filtered = df[df["PortfolioName"] == fund_name]

        if filtered.empty:
            raise FundNotFoundError(f"Fund '{fund_name}' not found.")

        return filtered
