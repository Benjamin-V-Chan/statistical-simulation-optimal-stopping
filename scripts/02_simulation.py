import csv

def simulate_stopping_strategy(payoffs, threshold=0.37):
    explore_count = int(len(payoffs) * threshold)
    max_explored = max(payoffs[:explore_count])
    for idx in range(explore_count, len(payoffs)):
        if payoffs[idx] > max_explored:
            return payoffs[idx], idx
    return payoffs[-1], len(payoffs) - 1

def save_simulation_results(file_path, results):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Payoff', 'Index'])
        writer.writerows(results)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simulate stopping strategies.")
    parser.add_argument("--input", type=str, required=True, help="Input CSV file path with payoffs")
    parser.add_argument("--threshold", type=float, default=0.37, help="Stopping threshold (default: 37%)")
    parser.add_argument("--output", type=str, required=True, help="Output CSV file path for simulation results")

    args = parser.parse_args()
    with open(args.input, mode='r') as file:
        payoffs = [float(row[0]) for row in csv.reader(file) if row[0] != 'Payoff']
    results = [simulate_stopping_strategy(payoffs, args.threshold)]
    save_simulation_results(args.output, results)