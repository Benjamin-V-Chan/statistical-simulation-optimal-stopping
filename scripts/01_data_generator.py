import random
import csv

def generate_payoff_values(n, mean=50, stddev=10, seed=None):
    if seed is not None:
        random.seed(seed)
    return [random.gauss(mean, stddev) for _ in range(n)]

def save_to_csv(file_path, data):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Payoff'])
        writer.writerows([[value] for value in data])

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate payoff values for the optimal stopping problem.")
    parser.add_argument("--n", type=int, required=True, help="Number of payoffs to generate")
    parser.add_argument("--mean", type=float, default=50, help="Mean of the payoff distribution")
    parser.add_argument("--stddev", type=float, default=10, help="Standard deviation of the payoff distribution")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--output", type=str, required=True, help="Output CSV file path")

    args = parser.parse_args()
    data = generate_payoff_values(args.n, args.mean, args.stddev, args.seed)
    save_to_csv(args.output, data)