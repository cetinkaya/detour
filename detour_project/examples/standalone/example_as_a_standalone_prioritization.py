import json
import math
import matplotlib.pyplot as pl
import subprocess

def plot_road(xvalues, yvalues, road_index, xmin, xmax, ymin, ymax):
    pl.rc('font', size=10)
    pl.plot(xvalues, yvalues, linewidth=10, color="#AAAAAA")
    pl.plot(xvalues, yvalues, linewidth=1, color="#FFFF40")
    pl.plot(xvalues[0], yvalues[0], linewidth=0, marker="o", markersize=5, color="black")
    pl.title(f"Road #{road_index}")
    pl.xlim([xmin, ymax])
    pl.ylim([ymin, ymax])

def main():
    p = subprocess.run(["detour",
                        "--functionality", "prioritization",
                        "--prioritization-ratio", "0.1",
                        "--executed-filepath", "example_executed.json",
                        "--not-executed-filepath", "example_not_executed.json",
                        "--output-filepath", "prioritization_result.json",
                        "--random-seed", "0"])
    # Create a plot
    roads = []
    with open('prioritization_result.json', 'r') as file:
        data = json.load(file)
        road_count = len(data)
        road_index = 0
        xmin = 200
        xmax = 0
        ymin = 200
        ymax = 0
        for entry in data:
            xvalues = [point["x"] for point in entry["road_points"]]
            yvalues = [point["y"] for point in entry["road_points"]]
            xmin = min([xmin, min(xvalues)])
            xmax = max([xmax, max(xvalues)])
            ymin = min([ymin, min(yvalues)])
            ymax = max([ymax, max(yvalues)])

        pl.figure(figsize=(8, 2 * math.ceil(road_count / 5)))
        for entry in data:
            road_index += 1
            xvalues = [point["x"] for point in entry["road_points"]]
            yvalues = [point["y"] for point in entry["road_points"]]
            pl.subplot(math.ceil(road_count / 5), 5, road_index)
            plot_road(xvalues, yvalues, road_index, xmin-20, xmax+20, ymin-20, ymax+20)

    pl.tight_layout()
    pl.savefig("plot_prioritization_result.png", dpi=300, bbox_inches='tight')
    pl.show()

main()
