import csv
import statistics

def load_simulation_results(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return [(float(row[0]), int(row[1])) for row in reader]

def calculate_summary_statistics(data):
    payoffs = [item[0] for item in data]
    return {
        "mean": statistics.mean(payoffs),
        "median": statistics.median(payoffs),
        "stddev": statistics.stdev(payoffs)
    }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze simulation results.")
    parser.add_argument("--input", type=str, required=True, help="Input CSV file path with simulation results")
    parser.add_argument("--output", type=str, required=False, help="Output text file path for summary")

    args = parser.parse_args()
    results = load_simulation_results(args.input)
    summary = calculate_summary_statistics(results)

    if args.output:
        with open(args.output, mode='w') as file:
            for key, value in summary.items():
                file.write(f"{key}: {value}\n")
    else:
        for key, value in summary.items():
            print(f"{key}: {value}")