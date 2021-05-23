import argparse
import matplotlib.pyplot as plt
import os.path
import math

argparser = argparse.ArgumentParser()
argparser.add_argument("--skip", type=int, default=1, help="x, where one out of x entries will be plotted")
argparser.add_argument("-s", "--scatter", action="store_true", help="draw scatter instead of curve plot")
argparser.add_argument("--start", type=float, default=0, help="the minimal x value to be plotted")
argparser.add_argument("--end", type=float, default=math.inf, help="the maximal x value to be plotted")
argparser.add_argument("--expected", type=str, default="", help="expected N(t) formula")
argparser.add_argument("input", type=str, help="the input file")
shell_args = argparser.parse_args()

if not os.path.exists(shell_args.input) or not os.path.isfile(shell_args.input):
  print("No such graph file")
  exit()

if shell_args.expected != "":
  N_func = eval("lambda x: " + shell_args.expected)
else:
  N_func = None

x_nums = []
y_nums = []
entry_count = 0
f = open(shell_args.input)
for line in f:
  if entry_count % shell_args.skip == 0:
    y, x = map(float, line.split())
    if x < shell_args.start or x > shell_args.end:
      continue
    x_nums.append(x)
    y_nums.append(y)
    if N_func:
      if x_nums[-1] != 0:
        y_nums[-1] /= N_func(x_nums[-1])
  entry_count += 1
f.close()

if not shell_args.scatter:
  plt.plot(x_nums, y_nums)
else:
  plt.scatter(x_nums, y_nums, s=2)
plt.show()

