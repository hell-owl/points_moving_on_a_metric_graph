import math
from xml.dom import minidom
import argparse
import os.path
from math import *
from collections import deque

class Edge:
    def __init__(self, source, target, length):
        self.source = source
        self.target = target
        self.length = length
        self.points = []
    
    def __str__(self):
        return "[edge from {} to {} with length {}]".format(self.source, self.target, self.length)
    
    def minimal_remaining_travel_time(self):
        """ returns the minimal among all points distance to the end
            points are moving from source to target
        """
        return min([self.length - p for p in self.points] or [math.inf])
    
    def is_point_at_the_end(self, point_pos):
        return abs(self.length - point_pos) < 0.000001
    
    def point_count(self):
        return len(self.points)
    
    def add_point(self, position):
        self.points.append(position)

class Graph:
    def __init__(self, vertex_number):
        self.vertex_number = vertex_number
        self.edge_lists = [[] for i in range(vertex_number)]
        self.age = 0 # time since the initial move of the points
    
    def add_edge(self, edge):
        self.edge_lists[edge.source].append(edge)
        return edge
    
    def minimal_remaining_travel_time(self):
        return min([min([edge.minimal_remaining_travel_time() for edge in edge_list] or [math.inf])
            for edge_list in self.edge_lists] or [math.inf])
    
    def step(self):
        delta_time = self.minimal_remaining_travel_time()
        self.age += delta_time
        future_new_points = set() # contains ids of vertices to add points to
        # move points
        for edge_list in self.edge_lists:
            for edge in edge_list:
                for point_index in range(len(edge.points)):
                    edge.points[point_index] += delta_time
        # delete points that reached the end and mark new points for creation
        for edge_list in self.edge_lists:
            for edge in edge_list:
                for point in edge.points:
                    if edge.is_point_at_the_end(point):
                        future_new_points.add(edge.target)
                edge.points = [point for point in edge.points if not edge.is_point_at_the_end(point)]
        # add new points
        for promise in future_new_points:
            for edge in graph.edge_lists[promise]:
                edge.points.append(0) # the point is added to the beginning of the edge
        
    def total_point_count(self):
        return sum([sum([edge.point_count() for edge in edge_list]) for edge_list in self.edge_lists])
    
    def how_old(self):
        return self.age



class FastEdge:
    def __init__(self, source, target, length, graph):
        self.source = source
        self.target = target
        self.length = length
        self.points = deque()
        self.graph = graph
    
    def __str__(self):
        return "[edge from {} to {} with length {}]".format(self.source, self.target, self.length)
    
    def minimal_remaining_travel_time(self):
        """ returns the minimal among all points distance to the end
            points are moving from source to target
        """
        if len(self.points) == 0:
          return math.inf
        else:
          lastPoint = self.points.pop()
          self.points.append(lastPoint)
          return self.length - (self.graph.age - lastPoint)
    
    def is_point_at_the_end(self, point_pos):
        return abs(self.length - point_pos) < 0.0001
    
    def reach_end(self):
        """ removes the points that already reached the end
            returns true if at least one point was removed
        """
        if len(self.points) == 0:
            return False
        else:
            while True:
                lastPoint = self.points.pop()
                if self.is_point_at_the_end(self.graph.age - lastPoint):
                    pass
                else:
                    self.points.append(lastPoint)
                    return False
                while len(self.points) > 0:
                    lastPoint = self.points.pop()
                    if not self.is_point_at_the_end(self.graph.age - lastPoint):
                        self.points.append(lastPoint)
                        break
                return True
    
    def point_count(self):
        return len(self.points)
    
    def add_point(self, position):
        self.points.appendleft(position)

class FastGraph:
    def __init__(self, vertex_number):
        self.vertex_number = vertex_number
        self.edge_lists = [[] for i in range(vertex_number)]
        self.age = 0 # time since the initial move of the points
        if shell_args.sympy:
            self.age = sympy.sqrt(0)
    
    def add_edge(self, edge):
        self.edge_lists[edge.source].append(edge)
        return edge
    
    def minimal_remaining_travel_time(self):
        return min([min([edge.minimal_remaining_travel_time() for edge in edge_list] or [math.inf])
            for edge_list in self.edge_lists] or [math.inf])
    
    def step(self):
        delta_time = self.minimal_remaining_travel_time()
        self.age += delta_time
        future_new_points = set() # contains ids of vertices to add points to
        # move points
        # (already done by changing the self.age property)
        # delete points that reached the end and mark new points for creation
        for edge_list in self.edge_lists:
            for edge in edge_list:
                if edge.reach_end():
                    future_new_points.add(edge.target)
        # add new points
        for promise in future_new_points:
            for edge in graph.edge_lists[promise]:
                edge.add_point(graph.age)
        
    def total_point_count(self):
        return sum([sum([edge.point_count() for edge in edge_list]) for edge_list in self.edge_lists])
    
    def how_old(self):
        return self.age


argparser = argparse.ArgumentParser()
argparser.add_argument("--iter", type=int, help="the number of modelling iterations")
argparser.add_argument("--sqrt", action="store_true", help="interpret each weight as the square of the desired value")
argparser.add_argument("-v", "--verbose", action="store_true", help="show additional data")
argparser.add_argument("--reduced", action="store_true", help="show less data")
argparser.add_argument("-f", "--fast", action="store_true", help="use fast algorythm")
argparser.add_argument("--sympy", action="store_true", help="use symbolic calculations")
argparser.add_argument("input", type=str, help="the input file")
shell_args = argparser.parse_args()

if shell_args.sympy:
    import sympy

if not os.path.exists(shell_args.input) or not os.path.isfile(shell_args.input):
  print("No such graph file")
  exit()

xml_graph = minidom.parse(shell_args.input)

nodes = xml_graph.getElementsByTagName("node")
edges = xml_graph.getElementsByTagName("edge")

if shell_args.fast:
    graph = FastGraph(len(nodes))
else:
    graph = Graph(len(nodes))

for edge_data in edges:
    if not shell_args.sqrt:
        edge_weight = eval(edge_data.attributes["weight"].value)
    else:
        if shell_args.sympy:
            edge_weight = sympy.sqrt(int(edge_data.attributes["weight"].value))
        else:
            edge_weight = float(edge_data.attributes["weight"].value) ** 0.5
    if shell_args.fast:
        the_edge = graph.add_edge(FastEdge(
            int(edge_data.attributes["source"].value),
            int(edge_data.attributes["target"].value),
            edge_weight, graph ))
    else:
        the_edge = graph.add_edge(Edge(
            int(edge_data.attributes["source"].value),
            int(edge_data.attributes["target"].value),
            edge_weight ))
    point_list = edge_data.attributes["upText"].value.split()
    for point in point_list:
        the_edge.add_point(float(point))

"""for i in range(graph.vertex_number):
    print("Node {}:".format(i))
    for edge in graph.edge_lists[i]:
        print(edge)"""

iterations = shell_args.iter or 10
for iter_number in range(iterations):
    if shell_args.reduced:
        if shell_args.sympy:
            print(graph.total_point_count(), graph.how_old().evalf())
        else:
            print(graph.total_point_count(), graph.how_old())
    else:
        print("total point count", graph.total_point_count(), "graph age", graph.how_old())
    if shell_args.verbose:
        print("minimal remaining time", graph.minimal_remaining_travel_time())
    graph.step()

