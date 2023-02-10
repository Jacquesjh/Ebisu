from typing import Callable

import numpy as np
import pandas as pd
from athena.src.core.services.optimizer import Optimizer
from pypfopt import HRPOpt
from pypfopt.risk_models import risk_matrix


class HRP(Optimizer):

    """

                                            Hierarchical Risk Parity


        Hierarchical Risk Parity is a novel portfolio optimization method developed by Marcos Lopez de Prado. It works
    differently when compared to the Efficient Frontier based method. However the principle of finding an optimal
    combination of risk and financial return is still the same.

    The algorithm works roughly as follows:

        1. From a universe of assets, form a distance matrix based on the correlation of the assets;
        2. Using this distance matrix, cluster the assets into a tree via hierarchical clustering;
        3. Within each branch of the tree, form the minimum variance portfolio (normally between just two assets);
        4. Iterate over each level, optimally combining the mini-portfolios at each node.

    The advantages of this are that it does not require the inversion of the covariance matrix as with traditional
    mean-variance optimization, and seems to produce diverse portfolios that perform well out of sample.

    In this implementation there a few parameters that can be tweaked when doing some parameters optimization via simulations
    and backtesting. They being:

        covariance_function: The algorithm for calculating the covariance matrix of the assets.

                    Implemented options: "sample_cov", "semicovariance", "exp_cov", "ledoit_wolf", "ledoit_wolf_constant_variance",
                                         "ledoit_wolf_single_factor", "ledoit_wolf_constant_correlation", "oracle_approximating".

        linkage_method: The algorithm that is used to created the hierarchical clustering tree.

                    Implemented options: "single", "complete", "average", "weighted", "centroid", "median", "ward".


    """

    historical_prices: pd.DataFrame
    hrp: HRPOpt
    covariance_function: str
    linkage_method: str

    def __init__(
        self,
        historical_prices: pd.DataFrame,
        covariance_function: str,
        linkage_method: str,
    ) -> None:
        self.linkage_method = linkage_method
        self.historical_prices = historical_prices.dropna(how="any")
        self.covariance_function = covariance_function
        self.hrp = self._optimize()

    def _get_covariance(self) -> pd.DataFrame:
        covariance = risk_matrix(
            self.historical_prices, method=self.covariance_function
        )
        covariance = self._fix_covariance_matrix(covariance=covariance)

        return covariance

    @staticmethod
    def _fix_covariance_matrix(covariance: pd.DataFrame) -> pd.DataFrame:
        covariance = covariance.replace(0, np.nan)

        for column in covariance.columns:
            values = covariance[column]
            num_nan = values.isna().sum()

            if num_nan >= len(values) - 1:
                covariance = covariance.drop(column, axis=1)
                covariance = covariance.drop(column, axis=0)

        return covariance

    def _optimize(self) -> HRPOpt:
        covariance = self._get_covariance()

        if len(covariance.columns) == 1:  # When there is only one asset
            hrp = pd.DataFrame(
                [1.0],
                columns=covariance.columns,
                index=[self.historical_prices.index[-1]],
            )

        else:
            hrp = HRPOpt(cov_matrix=covariance)
            hrp.optimize(linkage_method=self.linkage_method)

        return hrp

    def get_weights(self) -> pd.DataFrame:
        if type(self.hrp) == pd.DataFrame:
            weights = self.hrp

        else:
            weights = self.hrp.clean_weights(cutoff=0.01, rounding=3)

            num_tickers = len(weights.keys())
            date = self.historical_prices.index[-1]

            weights = pd.DataFrame(
                np.array(list(weights.values())).reshape((1, num_tickers)),
                columns=weights.keys(),
                index=[date],
            )

        return weights


def hrp_optimizer(df: pd.DataFrame, parameters: dict) -> Callable:
    covariance_function = parameters.get("covariance_function", None)
    linkage_method = parameters.get("linkage_method", None)
    prices = df["Close"]

    hrp = HRP(
        historical_prices=prices,
        covariance_function=covariance_function,
        linkage_method=linkage_method,
    )

    return hrp
