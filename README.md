# statistical-simulation-optimal-stopping

## Project Overview
The **Optimal Stopping Problem**, also known as the "Secretary Problem," explores the challenge of determining the best moment to stop observing a sequence of options and make a selection, given the goal of maximizing the probability of choosing the optimal option.

This simulation models a sequence of randomly generated payoff values and evaluates the performance of various stopping strategies.

---

## Folder Structure
```
project-root/
├── scripts/
│   ├── 01_data_generator.py      # Generates simulated payoff data
│   ├── 02_simulation.py   # Runs stopping strategy simulations
│   ├── 03_analysis.py            # Analyzes simulation results
│   ├── 04_visualization.py       # Visualizes results with graphs
├── outputs/                      # Stores generated outputs
│   ├── simulations.csv           # Simulation results
│   ├── analysis_summary.txt      # Summary of analysis
│   ├── graphs/                   # Visualization files
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

---

## Usage

### 1. Setup the Project:
- Clone the repository.
- Ensure you have Python installed.
- Install required dependencies using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 2. Generate Payoff Data:
Run the script to generate payoff values for the simulation. Specify the number of payoffs, mean, standard deviation, and output path.
```bash
python scripts/01_data_generator.py --n 100 --mean 50 --stddev 10 --seed 42 --output outputs/payoffs.csv
```

### 3. Simulate Stopping Strategy:
Run the simulation using the generated data. Specify the input file, stopping threshold, and output file for results.
```bash
python scripts/02_simulation.py --input outputs/payoffs.csv --threshold 0.37 --output outputs/simulations.csv
```

### 4. Analyze Results:
Analyze the simulation results to compute summary statistics (mean, median, standard deviation) and optionally save them to a file.
```bash
python scripts/03_analysis.py --input outputs/simulations.csv --output outputs/analysis_summary.txt
```

### 5. Visualize Results:
Generate visualizations (e.g., payoff distributions) from the simulation data and save them as images.
```bash
python scripts/04_visualization.py --input outputs/simulations.csv --output outputs/graphs/payoff_distribution.png
```

---

## Requirements
- Python 3.8+
- Required libraries:
  - matplotlib

Install all dependencies with:
```bash
pip install -r requirements.txt
```