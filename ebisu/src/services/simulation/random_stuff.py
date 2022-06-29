
import numpy as np


def get_random_strategy(total_tickers: int, num_filters: int, portfolio_size: int) -> dict:
    pipeline = dict()

    pipeline["filters"]   = get_random_filters(total_tickers = total_tickers, portfolio_size = portfolio_size, num_filters = num_filters)
    pipeline["optimizer"] = get_random_optimizer()

    return pipeline


def get_random_optimizer() -> dict:
    optimizer = dict()

    chosen_optimizer = np.random.choice(["hrp", "ewp"])
    opt_parameters = parameters_table_optimizer(optimizer_name = chosen_optimizer)
    optimizer[chosen_optimizer] = opt_parameters

    return optimizer


def parameters_table_optimizer(optimizer_name: str) -> dict:
    table = {
        "hrp" : hrp_parameter,
        "ewp" : ewp_parameter
    }

    optimizer_parameters = table.get(optimizer_name)()

    return optimizer_parameters


def hrp_parameter() -> dict:
    valid_functions = ["sample_cov", "semicovariance", "exp_cov", "oracle_approximating"]
    valid_linkage   = ["single", "complete", "average", "weighted", "centroid", "median", "ward"]

    opt = {
        "covariance_function": np.random.choice(valid_functions),
        "linkage_method"     : np.random.choice(valid_linkage)

    }

    return opt


def ewp_parameter() -> None:
    opt = None

    return opt


def get_random_filters(total_tickers: int, portfolio_size: int, num_filters: int) -> dict:
    filters = dict()
    previous_num_tickers = total_tickers

    for i in range(num_filters):
        if i == num_filters - 1:
            num_tickers      = portfolio_size
            possible_filters = ["volume", "momentum", "random", "sortino", "volatility", "sharpe"]

        else:
            num_tickers      = int((np.random.randint(20, 80)*previous_num_tickers)/100)
            possible_filters = ["volume", "max_price", "momentum", "random", "sortino", "volatility", "sharpe"]

            if num_tickers < portfolio_size:
                num_tickers = portfolio_size

        chosen_filter = np.random.choice(possible_filters)

        filter_parameters = parameters_table_filters(filter_name = chosen_filter, num_tickers = num_tickers)

        filters[f"{chosen_filter}->{i}"] = filter_parameters
        previous_num_tickers = num_tickers

    return filters


def parameters_table_filters(filter_name: str, num_tickers: int):
    table = {
        "volume"    : volume_parameters,
        "momentum"  : momentum_parameters,
        "max_price" : max_price_parameters,
        "sharpe"    : sharpe_parameters,
        "sortino"   : sortino_parameters,
        "random"    : random_parameters,
        "volatility": volatility_parameters
    }

    filter_parameters = table.get(filter_name)(num_tickers = num_tickers)

    return filter_parameters
 

def volume_parameters(num_tickers: int):
    parameters = dict()

    parameters["num_tickers"] = num_tickers
    parameters["days"]        = 5*np.random.randint(1, 28)

    return parameters


def momentum_parameters(num_tickers: int):
    parameters = dict()

    parameters["num_tickers"] = num_tickers
    parameters["months"]      = np.random.randint(1, 12)

    return parameters


def max_price_parameters(num_tickers: int):
    parameters = dict()

    parameters["cutoff"] = np.random.randint(5, 100)

    return parameters

    
def sharpe_parameters(num_tickers: int):
    parameters = dict()

    parameters["num_tickers"] = num_tickers

    return parameters

    
def sortino_parameters(num_tickers: int):
    parameters = dict()

    parameters["num_tickers"] = num_tickers

    return parameters

    
def random_parameters(num_tickers: int):
    parameters = dict()

    parameters["num_tickers"] = num_tickers

    return parameters
    

def volatility_parameters(num_tickers: int):
    parameters = dict()

    parameters["num_tickers"] = num_tickers

    return parameters