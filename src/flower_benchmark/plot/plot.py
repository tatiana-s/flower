# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Provides plotting functions."""

import os.path
import random
from enum import Enum
from pathlib import Path
from typing import List

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams["ps.useafm"] = True
matplotlib.rcParams["pdf.use14corefonts"] = True
matplotlib.rcParams["axes.axisbelow"] = True
matplotlib.rcParams["hatch.linewidth"] = 1.0
matplotlib.use("Agg")


ROOT_DIR = os.path.realpath(os.path.dirname(__file__) + "/../../..")
PLOT_DIR = ROOT_DIR + "/plot"

# If it does not exist create the output directory for the plots
Path(PLOT_DIR).mkdir(exist_ok=True)


MARKERSIZE = 3  # Size of the symbols on a linecharts


class LegendLoc(Enum):
    """Enumerates possible legend location in a plot."""

    UL = "upper left"
    UR = "upper right"
    LL = "lower left"
    LR = "lower right"
    UC = "upper center"
    LC = "lower center"
    CL = "center left"
    CR = "center right"


# Disable too many arguments for all functions
# pylint: disable=too-many-arguments


def final_path(dir_name: str, filename: str, suffix: str = "pdf") -> str:
    """Join path components and return as string."""
    filename_with_suffix = filename + "." + suffix

    if os.path.isabs(filename_with_suffix):
        return filename_with_suffix

    return os.path.join(dir_name, filename_with_suffix)


def plot_single_bar_chart(
    y_values: np.ndarray,
    tick_labels: List[str],
    x_label: str,
    y_label: str,
    filename: str = "single_bar_chart",
) -> str:
    """Plot and save a single bar chart."""

    x_values = np.arange(y_values.size)
    fig = plt.figure(figsize=(5, 3))
    ax_subplot = fig.add_subplot(111)

    barwidth = 0.7
    opacity = 1.0

    plt.bar(
        x_values,
        y_values,
        barwidth / 2,
        alpha=opacity,
        color=["black"],
        linewidth=1,
        edgecolor="black",
    )

    ax_subplot.spines["right"].set_visible(False)
    ax_subplot.spines["top"].set_visible(False)
    ax_subplot.xaxis.set_ticks_position("bottom")
    ax_subplot.yaxis.set_ticks_position("left")

    plt.ylabel(y_label, fontsize=16)
    plt.xlabel(x_label, fontsize=16)

    plt.xlim((-1, y_values.size))
    plt.ylim((0, 100))

    plt.grid(linestyle="dotted")
    # plt.ylim((0, 100))
    gca = plt.gca()
    gca.set_yticklabels(gca.get_yticks(), fontsize=16)
    ax_subplot.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%.0f"))

    ax_subplot.set_xticks([0, 1, 2, 3])

    ax_subplot.set_xticklabels(tick_labels, fontsize=14)

    fig.tight_layout()
    path = final_path(PLOT_DIR, filename)
    plt.savefig(path, dpi=1000, bbox_inches="tight", transparent=True)
    return path


def plot_bar_chart(
    y_values: List[np.ndarray],
    bar_labels: List[str],
    x_label: str,
    y_label: str,
    filename: str = "bar_chart",
) -> str:
    """Plot and save a bar chart.

    Note:
    Currently only supports len(y_values) == 2 but it should be easy to
    support more than 2 bars. Feel free to contribute.
    """

    x_values = np.arange(y_values[0].size)
    fig = plt.figure(figsize=(5, 3))
    ax_subplot = fig.add_subplot(111)

    barwidth = 0.7
    opacity = 1.0

    colors = ["r", "b"]

    rects = [
        plt.bar(
            x_values - barwidth * 0.25 * pow(-1, i),
            val,
            barwidth / len(y_values),
            alpha=opacity,
            color=[colors[i]],
            linewidth=1,
            edgecolor="black",
        )
        for i, val in enumerate(y_values)
    ]

    ax_subplot.spines["right"].set_visible(False)
    ax_subplot.spines["top"].set_visible(False)
    ax_subplot.xaxis.set_ticks_position("bottom")
    ax_subplot.yaxis.set_ticks_position("left")

    plt.ylabel(y_label, fontsize=16)
    plt.xlabel(x_label, fontsize=16)

    plt.xlim((-1, y_values[0].size))
    plt.ylim((0, 100))

    plt.grid(linestyle="dotted")
    # plt.ylim((0, 100))
    gca = plt.gca()
    gca.set_yticklabels(gca.get_yticks(), fontsize=16)
    ax_subplot.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%.0f"))

    ax_subplot.set_xticks([0, 1, 2])

    ax_subplot.set_xticklabels(("E=1", "E=2", "E=3"), fontsize=14)

    lgd = ax_subplot.legend(
        tuple([rect[0] for rect in rects]),
        tuple(bar_labels),
        fontsize=14,
        loc="best",
        ncol=2,
    )

    fig.tight_layout()
    path = final_path(PLOT_DIR, filename)
    plt.savefig(
        path,
        dpi=1000,
        bbox_inches="tight",
        bbox_extra_artists=(lgd,),
        transparent=True,
    )
    return path


def line_chart(
    lines: List[np.ndarray],
    labels: List[str],
    x_label: str,
    y_label: str,
    legend_location: LegendLoc = LegendLoc.UR,
    filename: str = "line_chart",
) -> str:
    """Plot and save a line chart."""

    assert len({line.size for line in lines}) == 1, "Each line must be of same size."

    x_values = range(0, len(lines[0]))
    plt.figure(figsize=(6, 4))
    ax_subplot = plt.subplot(111)
    symbols = ["-o", "-s", "-d", "-^", "-x", "-8", "-*", "-P"]

    for i, zipped in enumerate(zip(lines, labels)):
        line, label = zipped
        ax_subplot.plot(x_values, line, symbols[i], label=label, markersize=MARKERSIZE)

    plt.yticks(np.arange(0, 100, 10.0), fontsize=14)
    plt.xticks(np.arange(min(x_values), max(x_values) + 1, 10.0), fontsize=10)

    gca = plt.gca()
    gca.set_yticklabels(gca.get_yticks(), fontsize=10)
    ax_subplot.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%.0f"))

    plt.ylim((0, 101))
    plt.xlim((-1, len(x_values)))
    plt.legend(loc=legend_location.value, fontsize=14)
    # ax.set_xticklabels(('15s', '30s', '60s', '90s', '120s'), fontsize=15)
    plt.xlabel(x_label, fontsize=16)
    plt.ylabel(y_label, fontsize=16)

    path = final_path(PLOT_DIR, filename)
    plt.savefig(path, dpi=1000, bbox_inches="tight", transparent=True)
    return path


if __name__ == "__main__":
    e1 = np.array([random.uniform(0, i / 5) + 50 for i in range(100)])
    e5 = np.array([random.uniform(0, i / 5) + 25 for i in range(100)])
    e10 = np.array([random.uniform(0, i / 5) + 0 for i in range(100)])

    line_chart(
        [e1, e5, e10], ["E=1", "E=5", "E=10"], "Rounds", "Test Accuracy",
    )

    plot_bar_chart(
        [np.array([51.1, 52.3, 10.0]), np.array([59.3, 73.5, 80.0])],
        ["GPU-fast", "GPU-mixed"],
        "Local Epochs",
        "Training time",
    )

    plot_single_bar_chart(
        np.array([50.0, 70.0, 80.0]),
        ["10", "100", "1000"],
        "Number of Clients",
        "Test Accuracy",
    )