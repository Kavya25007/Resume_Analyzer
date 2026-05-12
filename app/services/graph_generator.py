import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

class GraphGenerator:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_bar(self, breakdown, filename="resume_graph.png"):
        path = os.path.join(self.output_dir, filename)
        labels = list(breakdown.keys())
        values = list(breakdown.values())

        plt.figure(figsize=(9, 5))
        bars = plt.bar(labels, values, color=["#4f46e5", "#06b6d4", "#10b981", "#f59e0b", "#ef4444"])
        plt.title("Resume Section Score Breakdown")
        plt.ylabel("Weighted Score")
        plt.ylim(0, 30)
        plt.grid(axis="y", alpha=0.25)

        for bar, val in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width() / 2, val + 0.3, str(val), ha="center", fontsize=9)

        plt.tight_layout()
        plt.savefig(path, dpi=200, bbox_inches="tight")
        plt.close()
        return path