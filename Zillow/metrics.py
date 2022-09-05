from typing import Tuple
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def measure_model(y_true, y_pred) -> Tuple[float, float, float]:
    """Measure the performance of a model.
    Parameters
    ----------
    y_true : array-like
        Ground truth (correct) target values.
    y_pred : array-like
        Estimated targets as returned by a classifier.
    Returns
    -------
    (float, float, float)
        Mean absolute error, mean squared error and R2 score.
    """
    return mean_absolute_error(y_true, y_pred), mean_squared_error(y_true, y_pred), r2_score(y_true, y_pred)


def print_measure(y_true, y_pred):
    """Print the performance of a model.
    Parameters
    ----------
    y_true : array-like
        Ground truth (correct) target values.
    y_pred : array-like
        Estimated targets as returned by a classifier.
    """
    print("Mean absolute error: {:.5f}".format(measure_model(y_true, y_pred)[0]))
    print(" Mean squared error: {:.5f}".format(measure_model(y_true, y_pred)[1]))
    print("           R2 score: {:.5f}".format(measure_model(y_true, y_pred)[2]))