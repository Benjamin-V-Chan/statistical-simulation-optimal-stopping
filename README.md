# statistical-simulation-optimal-stopping

## Project Overview
The **Optimal Stopping Problem**, also known as the "Secretary Problem," explores the challenge of determining the best moment to stop observing a sequence of options and make a selection, given the goal of maximizing the probability of choosing the optimal option.

This simulation models a sequence of randomly generated payoff values and evaluates the performance of various stopping strategies. The mathematical foundation includes:

### Mathematical Framework
Let a sequence of $n$ independent random variables $X_1, X_2, \dots, X_n$ represent the payoffs, where each $X_i$ is drawn from a known probability distribution $F(x)$ with probability density function $f(x)$. The goal is to select the largest $X_i$ with a single observation allowed per step.

Define:
- $T$ as the stopping rule, a function that maps the observed sequence $\{X_1, X_2, \dots, X_t\}$ to a binary decision space $\{\text{stop, continue}\}$.
- $P(\text{success})$ as the probability of selecting the global maximum.

#### Strategy and Optimality
The classical solution involves determining the optimal threshold $k = \lfloor n/e \rfloor$, where $e \approx 2.71828$ is the base of the natural logarithm. This threshold is derived by maximizing the success probability, given by:
$$P(\text{success}) = \sum_{k=1}^n \int_{-\infty}^\infty \Bigg[ \prod_{j=1}^{k-1} F(x) \prod_{j=k+1}^n (1 - F(x)) \Bigg] f(x) dx.$$

In this expression:
- $F(x)$ is the cumulative distribution function (CDF) of the payoff values.
- $\prod_{j=1}^{k-1} F(x)$ represents the probability that all observed values are less than $x$.
- $\prod_{j=k+1}^n (1 - F(x))$ represents the probability that the remaining values are less than $x$.

#### Why the $1/e$ Rule Works
The $1/e$ rule is optimal because it balances the trade-off between exploration and exploitation. The derivation is rooted in calculus and probability theory:
1. **Exploration Phase**:
   During the first $k = \lfloor n/e \rfloor$ steps, the algorithm observes values without selection. This ensures that the algorithm forms a representative sample of the distribution of payoffs.

2. **Exploitation Phase**:
   After the exploration phase, the algorithm selects the first value greater than the maximum observed in the exploration phase. This ensures that the probability of selecting the global maximum is maximized.

   To see why $k = \lfloor n/e \rfloor$ is optimal, consider the success probability:
   $$P(\text{success}) = \frac{1}{n} \sum_{k=1}^n (k-1) \int_0^1 x^{k-1} (1 - x)^{n-k} dx.$$

   For large $n$, this simplifies using Stirling's approximation and properties of the Beta function:
   $$P(\text{success}) \approx \int_0^1 e^{-x} dx = \frac{1}{e}.$$

3. **Proof by Optimization**:
   The $1/e$ rule minimizes the expected regret, defined as the difference between the global maximum and the selected value. By maximizing $P(\text{success})$, the algorithm guarantees asymptotically optimal performance as $n \to \infty$.

#### Generalization
To explore generalized stopping strategies, define a threshold proportion $p \in (0, 1)$. The threshold $k = \lfloor p \cdot n \rfloor$ allows for variations of the $1/e$ rule. The expected payoff $E[Y]$ for a strategy based on $p$ can be expressed as:
$$E[Y] = \int_0^1 \Bigg[\sum_{k=1}^{\lfloor p \cdot n \rfloor} x f(x) \prod_{j=1}^{k-1} F(x) \Bigg] dx.$$
Analyzing $E[Y]$ as a function of $p$ provides insights into the trade-offs between exploration and exploitation, and shows that $p = 1/e$ is uniquely optimal under uniform distributions.

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