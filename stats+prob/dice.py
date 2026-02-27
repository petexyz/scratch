import random
import sys
import math
from collections import Counter
from datetime import datetime

class DieSimulator:
    def __init__(self, sides):
        self.sides = sides
        self.counts = Counter()
        self.start_time = None
        self.end_time = None

    def roll_generator(self, tosses):
        """Generator yielding rolls one at a time (Memory efficient)."""
        for _ in range(tosses):
            yield random.randint(1, self.sides)

    def calculate_stats(self, tosses):
        """Calculates Mean, Variance, and Standard Deviation."""
        # Mean (μ) = Σ(x * frequency) / total_tosses
        mean = sum(side * count for side, count in self.counts.items()) / tosses
        
        # Variance (σ²) = Σ(count * (side - mean)²) / total_tosses
        variance = sum(count * (side - mean)**2 for side, count in self.counts.items()) / tosses
        
        # Standard Deviation (σ) = sqrt(variance)
        std_dev = math.sqrt(variance)
        
        return mean, variance, std_dev

    def run(self, tosses):
        """Executes simulation and tracks timing/stats."""
        self.start_time = datetime.now()
        for result in self.roll_generator(tosses):
            self.counts[result] += 1
        self.end_time = datetime.now()
        
        mean, var, std = self.calculate_stats(tosses)
        self.display_report(tosses, mean, var, std)

    def display_report(self, tosses, mean, var, std):
        duration = self.end_time - self.start_time
        
        print(f"\n{'='*55}")
        print(f"SIMULATION: {self.sides} SIDES | {tosses:,} TOSSES")
        print(f"{'='*55}")
        print(f"Timing details:")
        print(f"  Start:    {self.start_time.strftime('%H:%M:%S.%f')}")
        print(f"  End:      {self.end_time.strftime('%H:%M:%S.%f')}")
        print(f"  Duration: {duration}")
        print(f"{'-'*55}")
        
        print(f"{'Side':<10} | {'Occurrences':<15} | {'Percentage'}")
        print(f"{'-'*55}")
        for side in range(1, self.sides + 1):
            count = self.counts[side]
            print(f"{side:<10} | {count:<15} | {(count/tosses)*100:>9.2f}%")
        
        print(f"{'-'*55}")
        print(f"STATISTICAL SUMMARY:")
        print(f"  Mean (Average Roll):  {mean:.4f}")
        print(f"  Variance (σ²):        {var:.4f}")
        print(f"  Std Deviation (σ):    {std:.4f}")
        print(f"{'='*55}\n")

def get_params():
    """Checks CLI args [N X] or prompts the user."""
    try:
        if len(sys.argv) >= 3:
            return int(sys.argv[1]), int(sys.argv[2])
        n = int(input("Enter number of sides (N): "))
        x = int(input("Enter number of tosses (X): "))
        return n, x
    except ValueError:
        print("Invalid input. N and X must be integers.")
        sys.exit(1)

if __name__ == "__main__":
    n, x = get_params()
    sim = DieSimulator(n)
    sim.run(x)
