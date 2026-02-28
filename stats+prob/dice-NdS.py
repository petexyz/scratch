import random
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from collections import Counter
from datetime import datetime

class DicePoolSimulator:
    def __init__(self, sides, num_dice):
        self.sides = sides
        self.num_dice = num_dice
        self.counts = Counter()
        self.results_list = [] # Needed for smooth plotting

    def run(self, iterations):
        start_time = datetime.now()
        # Using a list here to feed the graphing engine efficiently
        self.results_list = [
            sum(random.randint(1, self.sides) for _ in range(self.num_dice))
            for _ in range(iterations)
        ]
        self.counts = Counter(self.results_list)
        end_time = datetime.now()
        
        self.display_stats(iterations, end_time - start_time)
        self.plot_distribution()

    def calculate_z_score(self, value, mean, std_dev):
        return (value - mean) / std_dev if std_dev > 0 else 0

    def display_stats(self, total, duration):
        mean = np.mean(self.results_list)
        std_dev = np.std(self.results_list)
        variance = np.var(self.results_list)
        median = np.median(self.results_list)
        mode = self.counts.most_common(1)[0][0]

        print(f"\n{'='*60}")
        print(f"SCENARIO: {self.num_dice}d{self.sides} | {total:,} ROLLS")
        print(f"{'='*60}")
        print(f"Duration: {duration}")
        print(f"Mean:     {mean:.2f}")
        print(f"Median:   {median:.1f}")
        print(f"Mode:     {mode}")
        print(f"Std Dev:  {std_dev:.4f}")
        print(f"Variance: {variance:.4f}")
        
        # Example Z-Score for the Max Roll
        max_roll = self.num_dice * self.sides
        z = self.calculate_z_score(max_roll, mean, std_dev)
        print(f"Z-Score (Max Roll {max_roll}): {z:.2f}")
        print(f"{'='*60}")

    def plot_distribution(self):
        data = self.results_list
        mu, std = norm.fit(data)

        # Create the plot
        plt.figure(figsize=(10, 6))
        
        # 1. Histogram (The actual data)
        # bins are set to align with integer dice sums
        bins = np.arange(self.num_dice - 0.5, (self.num_dice * self.sides) + 1.5, 1)
        plt.hist(data, bins=bins, density=True, alpha=0.6, color='skyblue', edgecolor='black', label='Actual Rolls')

        # 2. The Smooth Bell Curve (The theoretical Normal Distribution)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'r', linewidth=2, label=f'Normal Curve (μ={mu:.2f}, σ={std:.2f})')

        # Formatting
        title = f"Distribution of {self.num_dice}d{self.sides} ({len(data):,} rolls)"
        plt.title(title, fontsize=14)
        plt.xlabel('Sum of Dice')
        plt.ylabel('Probability Density')
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        
        print("Rendering graph... (Close window to exit)")
        plt.show()

def main():
    try:
        if len(sys.argv) >= 4:
            s, n, r = map(int, sys.argv[1:4])
        else:
            s = int(input("Sides (S): "))
            n = int(input("Dice (N): "))
            r = int(input("Rolls (R): "))
        
        sim = DicePoolSimulator(s, n)
        sim.run(r)
    except (ValueError, KeyboardInterrupt):
        print("\nExiting.")

if __name__ == "__main__":
    main()