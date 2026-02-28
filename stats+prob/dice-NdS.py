import random
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

class UltimateDiceSim:
    def __init__(self, sides, num_dice):
        self.sides = sides
        self.num_dice = num_dice
        self.results = []
        self.counts = {}
        self.mean = 0
        self.std = 0

    def run(self, iterations):
        # 1. Generate Data
        self.results = [sum(random.randint(1, self.sides) for _ in range(self.num_dice)) for _ in range(iterations)]
        self.mean, self.std = np.mean(self.results), np.std(self.results)
        
        unique, counts = np.unique(self.results, return_counts=True)
        self.counts = dict(zip(unique, counts))
        
        # 2. Setup Figure
        plt.ion()
        self.fig = plt.figure(figsize=(16, 8))
        gs = self.fig.add_gridspec(1, 2, width_ratios=[3, 1])
        
        self.ax1 = self.fig.add_subplot(gs[0, 0])
        self.ax_table = self.fig.add_subplot(gs[0, 1])
        
        self.update_graphics(None, None, "Ready", iterations)
        self.menu(iterations)

    def update_graphics(self, x_start, x_end, label_text, iterations):
        self.ax1.clear()
        self.ax_table.clear()
        
        # --- PLOT (Dual Y-Axis) ---
        bins = np.arange(self.num_dice - 0.5, (self.num_dice * self.sides) + 1.5, 1)
        self.ax1.hist(self.results, bins=bins, density=True, color='skyblue', edgecolor='black', alpha=0.4)
        
        x_axis = np.linspace(self.num_dice, self.num_dice * self.sides, 500)
        y_axis = norm.pdf(x_axis, self.mean, self.std)
        self.ax1.plot(x_axis, y_axis, 'r', linewidth=2)
        
        # Z-Score Labeling and Shading
        z_info = ""
        if x_start is not None or x_end is not None:
            fill_s = x_start if x_start is not None else self.num_dice
            fill_e = x_end if x_end is not None else self.num_dice * self.sides
            section = np.linspace(fill_s, fill_e, 200)
            self.ax1.fill_between(section, norm.pdf(section, self.mean, self.std), color='blue', alpha=0.4)
            
            # Draw Z-score lines and labels
            for val in [x_start, x_end]:
                if val is not None:
                    z = (val - self.mean) / self.std
                    self.ax1.axvline(val, color='darkblue', linestyle='--', alpha=0.7)
                    self.ax1.text(val, self.ax1.get_ylim()[1]*0.9, f'Z={z:.2f}', 
                                 rotation=90, verticalalignment='top', fontweight='bold')

        self.ax1.set_ylabel("Probability Density (Left)", color='blue')
        ax2 = self.ax1.twinx()
        ax2.set_ylim(self.ax1.get_ylim()[0] * iterations, self.ax1.get_ylim()[1] * iterations)
        ax2.set_ylabel("Actual Counts (Right)", color='black')

        self.ax1.set_title(f"{self.num_dice}d{self.sides} | {label_text}")

        # --- FREQUENCY TABLE ---
        self.ax_table.axis('off')
        table_data = []
        sums = sorted(self.counts.keys())
        for s in sums[:35]: # Displaying first 35 results
            count = self.counts[s]
            table_data.append([s, f"{count:,}", f"{(count/iterations)*100:.2f}%"])
        
        if len(sums) > 35: table_data.append(["...", "...", "..."])

        table = self.ax_table.table(cellText=table_data, colLabels=["Sum", "Count", "%"], 
                                    loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.5)

        plt.tight_layout(rect=[0, 0, 0.95, 1])
        plt.draw()

    def menu(self, iterations):
        while True:
            print("\n1. -inf to X | 2. X to Y | 3. X to inf | 4. Reset | 5. Exit")
            choice = input("Select: ")
            if choice == '5': break
            try:
                if choice == '1':
                    x = float(input("Enter X: "))
                    p = norm.cdf(x, self.mean, self.std)
                    self.update_graphics(None, x, f"P(X <= {x}) = {p*100:.2f}%", iterations)
                elif choice == '2':
                    x, y = float(input("Lower X: ")), float(input("Upper Y: "))
                    p = norm.cdf(y, self.mean, self.std) - norm.cdf(x, self.mean, self.std)
                    self.update_graphics(x, y, f"P({x} <= X <= {y}) = {p*100:.2f}%", iterations)
                elif choice == '3':
                    x = float(input("Enter X: "))
                    p = 1 - norm.cdf(x, self.mean, self.std)
                    self.update_graphics(x, None, f"P(X >= {x}) = {p*100:.2f}%", iterations)
                elif choice == '4':
                    self.update_graphics(None, None, "Cleared", iterations)
            except ValueError: print("Invalid input.")

if __name__ == "__main__":
    try:
        s = int(input("Sides (S): "))
        n = int(input("Dice (N): "))
        r = int(input("Rolls (R): "))
        UltimateDiceSim(s, n).run(r)
    except KeyboardInterrupt:
        print("\nExiting.")