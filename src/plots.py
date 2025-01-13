import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils import empirical_cdf
import streamlit as st


def plot_ctr(results: dict[str, np.ndarray],
             i: int, figsize: tuple[int, int] = (4, 3)) -> None:
    """
    Plot the ground truth user click-through rate (CTR) distribution.

    Args:
        results (dict[str, np.ndarray]): dictionary containing arrays of CTRs
            for both control and treatment groups.
        i (int): Index of the experiment to plot.
        figsize (tuple[int, int], optional): Figure size. Defaults to (4, 3).
    """
    ctrs_0 = results['ctrs_0'][i]
    ctrs_1 = results['ctrs_1'][i]

    sns.set_theme(style="darkgrid")
    sns.set_palette('rocket')
    fig, ax = plt.subplots(figsize=figsize)
    sns.histplot([ctrs_0, ctrs_1], kde=False, stat="probability",
                 common_norm=False, multiple="layer", bins=50, ax=ax)
    ax.set_title('Ground truth user CTR distribution')
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def plot_views(results: dict[str, np.ndarray], i: int,
               figsize: tuple[int, int] = (6, 4), fontsize: int = 12,
               bins: int = 30) -> None:
    """
    Plot the ground truth user views distribution.

    Args:
        results (dict[str, np.ndarray]): Dictionary containing arrays of views
            for both control and treatment groups.
        i (int): Index of the experiment to plot.
        figsize (tuple[int, int], optional): Figure size. Defaults to (6, 4).
        fontsize (int, optional): Font size for labels and title. Defaults to 12.
        bins (int, optional): Number of bins for the histogram. Defaults to 30.
    """
    # Validate inputs
    if not isinstance(results, dict) or 'views_0' not in results or 'views_1' not in results:
        raise ValueError("Results must be a dictionary containing 'views_0' and 'views_1'.")
    if not (0 <= i < len(results['views_0'])) or not (0 <= i < len(results['views_1'])):
        raise IndexError(f"Index {i} is out of bounds for the provided data.")

    views_0 = results['views_0'][i]
    views_1 = results['views_1'][i]

    # Set theme and figure
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=figsize)

    # Plot histograms
    sns.histplot([views_0, views_1], kde=False, stat="probability",
                 common_norm=False, multiple="layer", bins=bins, ax=ax,
                 palette="coolwarm", edgecolor="black")

    # Customize plot
    ax.set_title("Ground Truth User Views Distribution", fontsize=fontsize)
    ax.set_xlabel("Views", fontsize=fontsize)
    ax.set_ylabel("Probability", fontsize=fontsize)
    ax.legend(labels=["Control Group", "Treatment Group"], loc="upper right", fontsize=fontsize)
    ax.tick_params(axis="both", which="major", labelsize=fontsize)

    # Render with Streamlit
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)



def plot_p_hist(p_vals: np.ndarray, figsize: tuple[int, int] = (6, 4),
                fontsize: int = 12, bins: int = 20) -> None:
    """
    Plot the distribution of p-values.

    Args:
        p_vals (np.ndarray): Array of p-values.
        figsize (tuple[int, int], optional): Figure size. Defaults to (6, 4).
        fontsize (int, optional): Font size for tick labels. Defaults to 12.
        bins (int, optional): Number of bins for the histogram. Defaults to 20.
    """
    # Validate input
    if not isinstance(p_vals, np.ndarray):
        raise ValueError("p_vals must be a numpy array.")

    # Set theme and figure
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=figsize)

    # Plot histogram
    ax.hist(p_vals, bins=bins, density=True, color="skyblue", edgecolor="black")

    # Customize plot
    ax.set_title("Distribution of p-values", fontsize=fontsize)
    ax.set_xlabel("p-value", fontsize=fontsize)
    ax.set_ylabel("Density", fontsize=fontsize)
    ax.set_xlim(0, 1)
    ax.tick_params(axis="both", which="major", labelsize=fontsize)

    # Render with Streamlit
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

def plot_p_hist_all(results_pvals: dict[str, dict[str, np.ndarray]],
                    figsize: tuple[int, int] = (8, 5),
                    fontsize: int = 12, bins: int = 20, hist_alpha: float = 0.5) -> None:
    """
    Plot the distribution of p-values for multiple tests.

    Args:
        results_pvals (dict[str, dict[str, np.ndarray]]):
            Dictionary containing arrays of p-values for multiple tests.
        figsize (tuple[int, int], optional): Figure size. Defaults to (8, 5).
        fontsize (int, optional): Font size for tick labels. Defaults to 12.
        bins (int, optional): Number of bins for the histogram. Defaults to 20.
        hist_alpha (float, optional): Transparency of histogram bars. Defaults to 0.5.
    """
    # Validate input
    if not isinstance(results_pvals, dict) or not all(
        'p_vals' in test_data for test_data in results_pvals.values()
    ):
        raise ValueError("results_pvals must be a dictionary with 'p_vals' arrays.")

    # Set theme and figure
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=figsize)

    # Plot histogram for each test
    for test_name, test_data in results_pvals.items():
        ax.hist(test_data['p_vals'], bins=bins, density=True,
                alpha=hist_alpha, label=test_name, edgecolor="black")

    # Customize plot
    ax.set_title("Distribution of p-values (All Tests)", fontsize=fontsize)
    ax.set_xlabel("p-value", fontsize=fontsize)
    ax.set_ylabel("Density", fontsize=fontsize)
    ax.set_xlim(0, 1)
    ax.tick_params(axis="both", which="major", labelsize=fontsize)
    ax.legend(loc="upper right", fontsize=fontsize)

    # Render with Streamlit
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)



def plot_p_cdf(p_vals: np.ndarray, alpha: float = 0.05,
               figsize: tuple[int, int] = (6, 4),
               fontsize: int = 12, label_fontsize: int = 12) -> None:
    """
    Plot the empirical cumulative distribution function (CDF) of p-values.

    Args:
        p_vals (np.ndarray): Array of p-values.
        alpha (float, optional): Threshold for statistical significance. Defaults to 0.05.
        figsize (tuple[int, int], optional): Figure size. Defaults to (6, 4).
        fontsize (int, optional): Font size for tick labels. Defaults to 12.
        label_fontsize (int, optional): Font size for axis labels and title. Defaults to 12.
    """
    # Validate input
    if not isinstance(p_vals, np.ndarray):
        raise ValueError("p_vals must be a numpy array.")

    # Set theme and figure
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=figsize)

    # Compute empirical CDF
    p_vals_sorted, probs = empirical_cdf(p_vals)

    # Plot CDF
    ax.plot(p_vals_sorted, probs, label="Empirical CDF", lw=3)
    ax.axvline(x=alpha, color="red", linestyle="--", lw=2, label=f"Alpha = {alpha}")
    ax.plot([0, 1], [0, 1], color="gray", linestyle=":", lw=2, label="y = x (Uniform)")

    # Customize plot
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("p-value", fontsize=label_fontsize)
    ax.set_ylabel("Cumulative Probability", fontsize=label_fontsize)
    ax.set_title("Empirical CDF of p-values", fontsize=label_fontsize)
    ax.tick_params(axis="both", which="major", labelsize=fontsize)
    ax.legend(loc="lower right", fontsize=fontsize)

    # Render with Streamlit
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)



def plot_p_cdf_all(p_vals_dict: dict, alpha: float = 0.05,
                   figsize: tuple[int, int] = (8, 5),
                   fontsize: int = 12, label_fontsize: int = 12) -> None:
    """
    Plot the empirical CDF of p-values for multiple tests.

    Args:
        p_vals_dict (dict): Dictionary where keys are test names and values are dictionaries
            containing 'p_vals' arrays.
        alpha (float, optional): Threshold for statistical significance. Defaults to 0.05.
        figsize (tuple[int, int], optional): Figure size. Defaults to (8, 5).
        fontsize (int, optional): Font size for tick labels. Defaults to 12.
        label_fontsize (int, optional): Font size for axis labels and title. Defaults to 12.
    """
    # Validate input
    if not isinstance(p_vals_dict, dict) or not all(
        isinstance(v, dict) and "p_vals" in v for v in p_vals_dict.values()
    ):
        raise ValueError("p_vals_dict must be a dictionary with 'p_vals' arrays.")

    # Set theme and figure
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=figsize)

    # Plot CDF for each test
    for test_name, data in p_vals_dict.items():
        p_vals_sorted, probs = empirical_cdf(data['p_vals'])
        ax.plot(p_vals_sorted, probs, lw=3, label=test_name)

    # Add reference lines
    ax.axvline(x=alpha, color="red", linestyle="--", lw=2, label=f"Alpha = {alpha}")
    ax.plot([0, 1], [0, 1], color="gray", linestyle=":", lw=2, label="y = x (Uniform)")

    # Customize plot
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("p-value", fontsize=label_fontsize)
    ax.set_ylabel("Cumulative Probability", fontsize=label_fontsize)
    ax.set_title("Empirical CDF of p-values (All Tests)", fontsize=label_fontsize)
    ax.legend(loc="lower right", fontsize=fontsize)
    ax.tick_params(axis="both", which="major", labelsize=fontsize)

    # Render with Streamlit
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def plot_power(tests_results, alpha=0.05, figsize=(8, 4), fontsize=12,
               label_fontsize=12, bar_color="coolwarm"):
    """
    Plot the statistical power of tests.

    Args:
        tests_results (dict): Dictionary containing test results, where each test 
            has a 'p_vals' key with an array of p-values.
        alpha (float, optional): Significance level. Defaults to 0.05.
        figsize (tuple, optional): Figure size. Defaults to (8, 4).
        fontsize (int, optional): Font size for tick labels. Defaults to 12.
        label_fontsize (int, optional): Font size for labels. Defaults to 12.
        bar_color (str, optional): Matplotlib color palette for bars. Defaults to "coolwarm".
    """
    # Validate input
    if not isinstance(tests_results, dict) or not all(
        'p_vals' in test_data for test_data in tests_results.values()
    ):
        raise ValueError("tests_results must be a dictionary with 'p_vals' arrays.")

    # Calculate powers
    powers = {
        test_name: np.mean(test_data['p_vals'] < alpha)
        for test_name, test_data in tests_results.items()
    }

    # Sort powers for better readability
    sorted_tests = sorted(powers.items(), key=lambda x: x[1], reverse=True)
    test_names, power_values = zip(*sorted_tests)

    # Plotting
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=figsize)
    
    bar_colors = sns.color_palette(bar_color, n_colors=len(test_names))
    bars = ax.barh(test_names, power_values, color=bar_colors)
    
    # Add annotations
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.02, bar.get_y() + bar.get_height() / 2,
                f"{width:.2f}", va="center", fontsize=fontsize)

    # Set limits, labels, and title
    ax.set_xlim(0, 1)
    ax.set_xlabel("Power", fontsize=label_fontsize)
    ax.set_ylabel("Test Name", fontsize=label_fontsize)
    ax.set_title("Statistical Power of Tests", fontsize=label_fontsize)
    ax.tick_params(axis="both", which="major", labelsize=fontsize)

    # Adjust layout and show the plot
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
