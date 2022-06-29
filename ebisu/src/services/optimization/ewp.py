
from typing import Callable

import numpy as np
import pandas as pd

from athena.src.core.services.optimizer import Optimizer


class EWP(Optimizer):

    """

                                                Equal Weights Portfolio or Naive Portfolio


            The Equal Weights Portofoio, or simply the Naive Portfolio, is a simples portfolio managment technique
        that allocates money equally between the assets of the portfolio. This type of managment is often view as inefficient
        because it doesn't take into consideration the historical behaviour nor any statistical aspect of the assets but
        in many pratical case studies, this portfolio often performs very good when compared to more sophisticated one,
        like HRP, MVO, etc.

        This over simplistic model is, somewhat, consistente with other simple tecnhinque that end up outperfomring
        much more elaborated and sophisticated approaches. Therefore, dispite being trivial, I consider a valid option.

        There aren't any optimization options to be tweaked in this model, the weights are simply 1/N, where N is the number
        of assets.


    """


    def __init__(self, historical_prices: pd.DataFrame) -> None:
        self.historical_prices = historical_prices


    def get_weights(self) -> pd.DataFrame:
        weights = pd.DataFrame(columns = self.historical_prices.columns, index = [self.historical_prices.index[-1]])

        num_tickers = len(weights.columns)

        weights.values[:, :] = np.array([1/num_tickers]*num_tickers)

        return weights


def ewp_optimizer(df: pd.DataFrame, parameters: None) -> Callable:    
    prices = df["Close"]
    
    ewp = EWP(historical_prices = prices)

    return ewp
