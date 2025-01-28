import matplotlib.pyplot as plt
import csv

def plot_payoff_distribution(data, output_path):
    payoffs = [item[0] for item in data]
    plt.hist(payoffs, bins=20, color='blue', alpha=0.7)
    plt.title('Payoff Distribution')
    plt.xlabel('Payoff')
    plt.ylabel('Frequency')
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Visualize simulation results.")
    parser.add_argument("--input", type=str, required=True, help="Input CSV file path with simulation results")
    parser.add_argument("--output", type=str, required=True, help="Output path for the histogram graph")

    args = parser.parse_args()
    with open(args.input, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        data = [(float(row[0]), int(row[1])) for row in reader]

    plot_payoff_distribution(data, args.output)