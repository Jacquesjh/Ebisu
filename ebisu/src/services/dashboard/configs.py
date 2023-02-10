import json
import os

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "tickers.json")

with open(file_path) as f:
    TICKERS_AVAILABLE = json.load(f)


DOMAINS_AVAILABLE = ["stocks", "variable etfs", "fixed etfs"]
SECTORS_AVAILABLE = [
    "Servicos Comerciais",
    "Comunicacoes",
    "Consumiveis Duraveis",
    "Consumiveis nao Duraveis",
    "Consumo de Servicos",
    "Sevicos de Logistica",
    "Tecnologia Eletronica",
    "Mineirais Energeticos",
    "Financeiro",
    "Servicos de Saude",
    "Tecnologia em Saude",
    "Servicos Industriais",
    "Minerais nao Energeticos",
    "Industrias de Processamento",
    "Produtor Manufatureiro",
    "Varejo",
    "Servico de Tecnologia",
    "Transporte",
    "Servico Publico",
]
RULES_AVAILABLE = [
    "include_tickers",
    "include_sectors",
    "exclude_tickers",
    "exclude_sectors",
]
CONSTRAINTS_AVAILABLE = ["invest_sections", "invest_tickers"]
FILTERS_AVAILABLE = [
    "Volume",
    "Momentum",
    "Random",
    "Min_Price",
    "Max_Price",
    "RoMad",
    "Volatility",
    "Sharpe",
    "Sortino",
]
OPTIMIZERS_AVAILABLE = ["HRP", "EWP"]

RULES_SECUNDARY_OPTIONS = {
    "include_tickers": ["tickers"],
    "include_sectors": ["sectors"],
    "exclude_tickers": ["tickers"],
    "exclude_sectors": ["sectors"],
}

FILTERS_SECUNDARY_OPTIONS = {
    "Volume": ["num_tickers", "months"],
    "Momentum": ["num_tickers", "months"],
    "Random": ["num_tickers"],
    "Min_Price": ["cutoff"],
    "Max_Price": ["cutoff"],
    "RoMad": ["num_tickers"],
    "Volatility": ["num_tickers"],
    "Sharpe": ["num_tickers"],
    "Sortino": ["num_tickers"],
}

OPTIMIZERS_SECUNDARY_OPTIONS = {
    "HRP": {
        "covariance_function": [
            "sample_cov",
            "semicovariance",
            "exp_cov",
            "ledoit_wolf",
            "ledoit_wolf_constant_variance",
            "ledoit_wolf_single_factor",
            "ledoit_wolf_constant_correlation",
            "oracle_approximating",
        ],
        "linkage_method": [
            "single",
            "complete",
            "average",
            "weighted",
            "centroid",
            "median",
            "ward",
        ],
    },
    "EWP": {},
}
