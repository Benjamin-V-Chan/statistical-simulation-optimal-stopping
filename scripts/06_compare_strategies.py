import argparse
import csv
import random
import statistics

import matplotlib.pyplot as plt


def load_payoffs(file_path):
    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        next(reader, None)
        payoffs = []
        for row in reader:
            if not row:
                continue
            payoffs.append(float(row[0]))
    return payoffs


def simulate_stopping_strategy(payoffs, threshold=0.37):
    explore_count = int(len(payoffs) * threshold)
    max_explored = max(payoffs[:explore_count])
    for idx in range(explore_count, len(payoffs)):
        if payoffs[idx] > max_explored:
            return payoffs[idx], idx
    return payoffs[-1], len(payoffs) - 1


def simulate_all_strategies(payoffs, runs, threshold=0.37, seed=None):
    if not payoffs:
        raise ValueError("Payoffs list is empty.")
    shuffle_rng = random.Random(seed)
    choice_seed = None if seed is None else seed + 1
    choice_rng = random.Random(choice_seed)
    results = {
        "secretary": [],
        "random": [],
        "first": [],
        "last": [],
    }
    for _ in range(runs):
        shuffled = payoffs[:]
        shuffle_rng.shuffle(shuffled)
        payoff, _ = simulate_stopping_strategy(shuffled, threshold)
        results["secretary"].append(payoff)
        results["first"].append(shuffled[0])
        results["last"].append(shuffled[-1])
        idx = choice_rng.randrange(len(shuffled))
        results["random"].append(shuffled[idx])
    return results


def summarize(values):
    stddev = statistics.stdev(values) if len(values) > 1 else 0.0
    return {
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "stddev": stddev,
    }


def build_strategy_meta(threshold):
    percent = int(round(threshold * 100))
    return {
        "secretary": {"label": f"{percent}% rule", "color": "#264653"},
        "random": {"label": "Random choice", "color": "#f4a261"},
        "first": {"label": "Always first", "color": "#2a9d8f"},
        "last": {"label": "Always last", "color": "#e76f51"},
    }


def plot_comparison(results, summary, meta, output_path):
    order = ["secretary", "random", "first", "last"]
    labels = [meta[name]["label"] for name in order]
    colors = [meta[name]["color"] for name in order]
    data = [results[name] for name in order]
    means = [summary[name]["mean"] for name in order]
    stddevs = [summary[name]["stddev"] for name in order]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    box = axes[0].boxplot(data, labels=labels, patch_artist=True, showmeans=True)
    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    axes[0].set_title("Payoff distribution by strategy")
    axes[0].set_ylabel("Payoff")

    axes[1].bar(labels, means, yerr=stddevs, color=colors, alpha=0.7, capsize=5)
    axes[1].set_title("Mean payoff (std dev)")
    axes[1].set_ylabel("Payoff")

    fig.suptitle("Stopping Strategy Comparison")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(output_path)
    plt.close(fig)


def format_summary(summary, meta):
    lines = []
    order = ["secretary", "random", "first", "last"]
    for name in order:
        stats = summary[name]
        label = meta[name]["label"]
        lines.append(
            f"{label}: mean={stats['mean']:.4f}, median={stats['median']:.4f}, stddev={stats['stddev']:.4f}"
        )
    best = max(order, key=lambda key: summary[key]["mean"])
    lines.append(f"Best by mean payoff: {meta[best]['label']}")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare stopping strategies with shared simulation settings."
    )
    parser.add_argument(
        "--input", type=str, required=True, help="Input CSV file path with payoffs"
    )
    parser.add_argument(
        "--threshold", type=float, default=0.37, help="Stopping threshold (default: 37%)"
    )
    parser.add_argument(
        "--runs", type=int, default=1000, help="Number of simulation runs"
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--output", type=str, required=True, help="Output image path for comparison plot"
    )
    parser.add_argument(
        "--summary-output",
        type=str,
        required=False,
        help="Optional output text file path for summary",
    )

    args = parser.parse_args()
    payoffs = load_payoffs(args.input)
    results = simulate_all_strategies(payoffs, args.runs, args.threshold, args.seed)
    meta = build_strategy_meta(args.threshold)
    summary = {name: summarize(values) for name, values in results.items()}

    plot_comparison(results, summary, meta, args.output)
    summary_text = format_summary(summary, meta)

    if args.summary_output:
        with open(args.summary_output, mode="w") as file:
            file.write(summary_text + "\n")
    else:
        print(summary_text)
