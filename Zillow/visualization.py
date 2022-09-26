from typing import Tuple
from mpl_toolkits.basemap import Basemap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numbers
import seaborn as sns

from Zillow.data import property_land_use_type
from Zillow.types import MoreFeatures as mft

def create_labels_for_non_zero_land_use_types(df: pd.DataFrame) -> Tuple[dict, dict]:
    labels = {}
    color_map = {}
    for i, (key, label) in enumerate(property_land_use_type.items()):
        if len(df[df[mft.land_use_label.value] == label]) > 0:
            labels[key] = label
            color_map[label] = i
    return labels, color_map


class ZillowMap(Basemap):

    def __init__(self, ax):
        super().__init__(projection='lcc', resolution='f',
            lat_0=34, lon_0=-118.3,
            width=230000, height=250000, ax=ax)
        self.draw_map_basics()

    def draw_map_basics(self):
        self.drawmapboundary(fill_color='#d8eaf3')
        self.fillcontinents(color='#f6fbd7',lake_color='#d8eaf3')
        self.drawcoastlines(color='gray')
        self.drawcounties(color='darkgrey', linewidth=.3)


def plot_heatmap(df):
    fig, ax = plt.subplots(figsize=(30, 30))

    sns.heatmap(data=df.corr(),
                mask=np.triu(np.ones_like(df.corr(), dtype=bool)),
                vmax=1.0,
                vmin=-1.0,
                center=0,
                square=True,
                annot=True,
                fmt=".2f",
                annot_kws={"size": 9},
                linewidths=.5,
                ax=ax)


def plot_random_forest_feature_importance(df, rf):
    feature_names = df.columns.to_list()

    fig, ax = plt.subplots(figsize=(80,5))
    ax.bar(range(0,df.shape[1]), rf.feature_importances_)
    ax.set_title("Feature Importances")
    ax.set_xticks(range(df.shape[1]))
    ax.set_xticklabels(feature_names)
    ax.grid()


def plot_grid_search_validation_curve(grid, param_to_vary,
                                      title='Validation Curve', ylim=None,
                                      xlim=None, log=None):
    """Plots train and cross-validation scores from a GridSearchCV instance's
    best params while varying one of those params."""

    df_cv_results = pd.DataFrame(grid.cv_results_)
    train_scores_mean = df_cv_results['mean_train_score']
    valid_scores_mean = df_cv_results['mean_test_score']
    train_scores_std = df_cv_results['std_train_score']
    valid_scores_std = df_cv_results['std_test_score']

    param_cols = [c for c in df_cv_results.columns if c[:6] == 'param_']
    param_ranges = [grid.param_grid[p[6:]] for p in param_cols]
    param_ranges_lengths = [len(pr) for pr in param_ranges]

    train_scores_mean = np.array(train_scores_mean).reshape(*param_ranges_lengths)
    valid_scores_mean = np.array(valid_scores_mean).reshape(*param_ranges_lengths)
    train_scores_std = np.array(train_scores_std).reshape(*param_ranges_lengths)
    valid_scores_std = np.array(valid_scores_std).reshape(*param_ranges_lengths)

    param_to_vary_idx = param_cols.index('param_{}'.format(param_to_vary))

    slices = []
    for idx, param in enumerate(grid.best_params_):
        if (idx == param_to_vary_idx):
            slices.append(slice(None))
            continue
        best_param_val = grid.best_params_[param]
        idx_of_best_param = 0
        if isinstance(param_ranges[idx], np.ndarray):
            idx_of_best_param = param_ranges[idx].tolist().index(best_param_val)
        else:
            idx_of_best_param = param_ranges[idx].index(best_param_val)
        slices.append(idx_of_best_param)

    train_scores_mean = train_scores_mean[tuple(slices)]
    valid_scores_mean = valid_scores_mean[tuple(slices)]
    train_scores_std = train_scores_std[tuple(slices)]
    valid_scores_std = valid_scores_std[tuple(slices)]

    plt.clf()

    plt.title(title)
    plt.xlabel(param_to_vary)
    plt.ylabel('Score')

    if (ylim is None):
        plt.ylim(0.0, 1.1)
    else:
        plt.ylim(*ylim)

    if (not (xlim is None)):
        plt.xlim(*xlim)

    lw = 2

    plot_fn = plt.plot
    if log:
        plot_fn = plt.semilogx

    param_range = param_ranges[param_to_vary_idx]
    if (not isinstance(param_range[0], numbers.Number)):
        param_range = [str(x) for x in param_range]
    plot_fn(param_range, train_scores_mean, label='Training score', color='r',
            lw=lw)
    plt.fill_between(param_range, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color='r', lw=lw)
    plot_fn(param_range, valid_scores_mean, label='Cross-validation score',
            color='b', lw=lw)
    plt.fill_between(param_range, valid_scores_mean - valid_scores_std,
                     valid_scores_mean + valid_scores_std, alpha=0.1,
                     color='b', lw=lw)

    plt.legend(loc='lower right')

    plt.show()