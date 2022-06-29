"""

    DON'T use "sample covariance matrix" because it has a high estimation error, which is particularly dangerous
    in mean-variance optimization because the optimizer is likely to give excess weight to these erroneous estimates.

"""