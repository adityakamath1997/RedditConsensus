from __future__ import annotations

from io import BytesIO
import base64
from typing import Dict, List, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from backend.app.schemas.answer_frequency_schema import FrequencyOutput


def _sorted_top_items(data: Dict[str, int], max_bars: int):
    items = [
        (str(label), int(value))
        for label, value in data.items()
        if isinstance(label, str) and isinstance(value, (int, float)) and int(value) >= 0
    ]
    items.sort(key=lambda x: x[1], reverse=True)
    return items[:max(1, max_bars)] if max_bars else items


def _plot_to_base64_hbar(title: str, items: List[Tuple[str, int]]):
    labels = [label for label, _ in items]
    values = [value for _, value in items]

    # Fallback
    if not labels:
        labels = ["No data"]
        values = [0]

    height = max(2.5, 0.4 * len(labels) + 1.0)
    fig, ax = plt.subplots(figsize=(10, height))
    ax.barh(range(len(labels)), values, color="#4C78A8")
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_title(title)
    ax.set_xlabel("Count")

    for i, v in enumerate(values):
        ax.text(v + max(values) * 0.01 if max(values) else 0.05, i, str(v), va="center")

    plt.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def build_histogram_images(
    metrics: FrequencyOutput, *, max_bars: int = 15
):

    top_freq = _sorted_top_items(metrics.answer_frequency, max_bars)
    top_likes = _sorted_top_items(metrics.like_count, max_bars)

    freq_png = _plot_to_base64_hbar("Answer Frequency (Top)", top_freq)
    likes_png = _plot_to_base64_hbar("Total Upvotes (Top)", top_likes)

    return {
        "answer_frequency_png": freq_png,
        "like_count_png": likes_png,
    }


