import argparse
import csv
import os
import random

import matplotlib.pyplot as plt

STRATEGIES = {
    "random": {"label": "Random choice", "color": "#f4a261"},
    "first": {"label": "Always first", "color": "#2a9d8f"},
    "last": {"label": "Always last", "color": "#e76f51"},
}


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


def simulate_other_strategies(payoffs, runs, seed=None):
    if not payoffs:
        raise ValueError("Payoffs list is empty.")
    shuffle_rng = random.Random(seed)
    choice_seed = None if seed is None else seed + 1
    choice_rng = random.Random(choice_seed)
    results = {name: [] for name in STRATEGIES}
    for _ in range(runs):
        shuffled = payoffs[:]
        shuffle_rng.shuffle(shuffled)
        results["first"].append(shuffled[0])
        results["last"].append(shuffled[-1])
        idx = choice_rng.randrange(len(shuffled))
        results["random"].append(shuffled[idx])
    return results


def resolve_hist_range(results, range_min, range_max):
    if range_min is not None and range_max is not None:
        return range_min, range_max
    values = []
    for values_list in results.values():
        values.extend(values_list)
    if not values:
        raise ValueError("No results to plot.")
    data_min = min(values)
    data_max = max(values)
    return (
        data_min if range_min is None else range_min,
        data_max if range_max is None else range_max,
    )


def plot_histograms(results, output_dir, bins, range_min, range_max):
    os.makedirs(output_dir, exist_ok=True)
    for name, meta in STRATEGIES.items():
        values = results[name]
        plt.figure()
        plt.hist(
            values,
            bins=bins,
            range=(range_min, range_max),
            color=meta["color"],
            alpha=0.7,
            edgecolor="black",
        )
        plt.title(f"{meta['label']} Payoff Distribution")
        plt.xlabel("Payoff")
        plt.ylabel("Frequency")
        output_path = os.path.join(output_dir, f"{name}_hist.png")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot histograms for alternative stopping strategies."
    )
    parser.add_argument(
        "--input", type=str, required=True, help="Input CSV file path with payoffs"
    )
    parser.add_argument(
        "--runs", type=int, default=1000, help="Number of simulation runs"
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument("--bins", type=int, default=20, help="Histogram bins")
    parser.add_argument(
        "--range-min",
        type=float,
        default=None,
        help="Optional histogram range minimum",
    )
    parser.add_argument(
        "--range-max",
        type=float,
        default=None,
        help="Optional histogram range maximum",
    )
    parser.add_argument(
        "--output-dir", type=str, required=True, help="Output directory for histograms"
    )

    args = parser.parse_args()
    payoffs = load_payoffs(args.input)
    results = simulate_other_strategies(payoffs, args.runs, args.seed)
    range_min, range_max = resolve_hist_range(results, args.range_min, args.range_max)
    plot_histograms(results, args.output_dir, args.bins, range_min, range_max)
