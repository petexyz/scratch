import random
import sys
import math
from collections import Counter
from datetime import datetime

class DicePoolSimulator:
    def __init__(self, sides, num_dice):
        self.sides = sides
        self.num_dice = num_dice
        self.counts = Counter()
        self.start_time = None
        self.end_time = None

    def roll_generator(self, iterations):
        for _ in range(iterations):
            yield sum(random.randint(1, self.sides) for _ in range(self.num_dice))

    def calculate_stats(self, total_rolls):
        if total_rolls == 0: return 0, 0, 0
        mean = sum(val * count for val, count in self.counts.items()) / total_rolls
        variance = sum(count * (val - mean)**2 for val, count in self.counts.items()) / total_rolls
        std_dev = math.sqrt(variance)
        return mean, variance, std_dev

    def get_distribution_label(self):
        if self.num_dice == 1:
            return "UNIFORM (All outcomes equally likely)"
        elif self.num_dice == 2:
            return "TRIANGULAR (Sum of two independent variables)"
        else:
            return "NORMAL / GAUSSIAN (Central Limit Theorem in effect)"

    def print_ascii_graph(self, iterations, max_width=50):
        if not self.counts: return
        print(f"\nDISTRIBUTION TYPE: {self.get_distribution_label()}")
        print("-" * 65)
        
        max_freq = max(self.counts.values())
        for s in range(self.num_dice, (self.num_dice * self.sides) + 1):
            count = self.counts[s]
            bar_length = int((count / max_freq) * max_width) if max_freq > 0 else 0
            print(f"{s:>4} | {'█' * bar_length} {count}")
        print("-" * 65)

    def run(self, iterations):
        self.start_time = datetime.now()
        try:
            for total_sum in self.roll_generator(iterations):
                self.counts[total_sum] += 1
            self.end_time = datetime.now()
            
            actual_rolls = sum(self.counts.values())
            m, v, sd = self.calculate_stats(actual_rolls)
            
            # Header
            print(f"\n{'='*65}\nSCENARIO: {self.num_dice}d{self.sides} | {actual_rolls:,} ROLLS\n{'='*65}")
            print(f"Start: {self.start_time.strftime('%H:%M:%S.%f')}")
            print(f"End:   {self.end_time.strftime('%H:%M:%S.%f')}")
            print(f"Dur:   {self.end_time - self.start_time}\n{'-'*65}")
            
            # Table
            print(f"{'Sum':<8} | {'Occurrences':<15} | {'Percentage'}")
            for s in range(self.num_dice, (self.num_dice * self.sides) + 1):
                c = self.counts[s]
                print(f"{s:<8} | {c:<15} | {(c/actual_rolls)*100:>10.2f}%")
            
            print(f"{'-'*65}\nSTATS: Mean: {m:.2f} | Var: {v:.2f} | StdDev: {sd:.2f}")
            self.print_ascii_graph(actual_rolls)

        except KeyboardInterrupt:
            print("\nExiting.")

def main():
    try:
        # CLI Args: S N R
        if len(sys.argv) >= 4:
            s, n, r = map(int, sys.argv[1:4])
        else:
            s = int(input("Sides (S): "))
            n = int(input("Dice (N): "))
            r = int(input("Rolls (R): "))
        
        DicePoolSimulator(s, n).run(r)
    except (ValueError, EOFError):
        print("\nInvalid input. Use integers.")

if __name__ == "__main__":
    main()
