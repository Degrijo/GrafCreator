from PyQt5.QtWidgets import QMessageBox
from random import choice
import networkx as nx


class Graf:
    def __init__(self, node_rad):  # делать граф взвешенным, если добавляет вес ребру
        self.vertexes = []
        self.weighted = False
        self.node_rad = node_rad

    def get_vertex(self, x, y):
        selected = False
        for vert in self.vertexes:
            if vert.x - self.node_rad < x < vert.x + self.node_rad and vert.y - self.node_rad < y < vert.y + self.node_rad:
                selected = vert
        return selected

    def add_vertex(self, x, y):
        self.vertexes.append(Vertex(str(len(self.vertexes)), x, y))

    def add_edge(self, vertex1, vertex2, oriented=False):
        if vertex1 in self.vertexes and vertex2 in self.vertexes:
            self.vertexes[self.vertexes.index(vertex1)].edges.append(Edge(vertex1, vertex2, oriented))
            if not oriented:
                self.vertexes[self.vertexes.index(vertex2)].edges.append(Edge(vertex2, vertex1, oriented))
        else:
            print("There aren't such vertexes")

    def del_edge(self, vertex1, vertex2, oriented=False):
        for edge in vertex1.edges:
            if edge.vertex2 == vertex2:
                vertex1.edges.remove(edge)
                break
        if not oriented:
            for edge in vertex2.edges:
                if edge.vertex2 == vertex1:
                    vertex2.edges.remove(edge)
                    break

    def del_vertex(self, vertex):
        for edge in vertex.edges:
            self.del_edge(vertex, edge.vertex2, edge.oriented)
        self.vertexes.remove(vertex)

    def get_edge(self, vertex1, vertex2):
        selected = False
        for edge in vertex1.edges:
            if edge.vertex2 == vertex2:
                selected = edge
        return selected

    def radius_diameter(self):
        g = nx.Graph()
        for vert in self.vertexes:
            for edge in vert.edges:
                g.add_edge(vert, edge.vertex2)
        if len(g.nodes) > 0:
            return nx.radius(g), nx.diameter(g)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Empty graph")
            msg.setWindowTitle("Graph doesn't has any nodes")
            msg.setDetailedText("You can't calculate it in empty graph!")
            msg.setStandardButtons(QMessageBox.Ok)

    def my_radius_diameter(self):
        if len(self.vertexes) is not 0:
            vert_with_min_edges = [-1]
            roads = {}
            for vert in self.vertexes:
                if vert_with_min_edges == [-1]:
                    if len(vert.edges) > 0:
                        vert_with_min_edges = [vert]
                else:
                    if 0 < len(vert.edges) < len(vert_with_min_edges[0].edges):
                        vert_with_min_edges = [vert]
                    elif len(vert_with_min_edges[0].edges) == len(vert.edges):
                        vert_with_min_edges.append(vert)
            if len(vert_with_min_edges) == 1:
                if vert_with_min_edges == [-1]:
                    print("Too little edges")
                    return 0, 0
                else:
                    i = len(vert_with_min_edges) + 1
                    while True:
                        for vert in self.vertexes:
                            if vert_with_min_edges[0] == i:
                                vert_with_min_edges.append(vert)
                        if len(vert_with_min_edges) > 1:
                            break
                        i += 1

            for vert in vert_with_min_edges:
                times = 0
                for vert1 in self.vertexes:
                    vert1.check = True
                    for edge in vert1.edges:
                        edge.check = True
                        if edge.oriented:
                            times += 1
                        else:
                            times += 0.5
                old_way = []
                for i in range(int(times) * 2):
                    vert1 = vert
                    road = {}
                    while vert1 not in vert_with_min_edges[vert_with_min_edges.index(vert) + 1:]:
                        free_edges = []
                        for edge in vert1.edges:
                            if edge.check and edge.vertex2.check:
                                free_edges.append(edge)
                        if len(free_edges) is 1:
                            vert1.check = False
                            road.setdefault(free_edges[0], "choice")
                            free_edges[0].check = False
                            if not free_edges[0].oriented:
                                self.get_edge(free_edges[0].vertex2, vert1).check = False
                            vert1 = free_edges[0].vertex2
                        elif len(free_edges) >= 2:
                            vert1.check = False
                            road.setdefault(choice(free_edges), "random")
                            rand_edge = list(road.keys())[-1]
                            rand_edge.check = False
                            if not rand_edge.oriented:
                                self.get_edge(rand_edge.vertex2, vert1).check = False
                            vert1 = rand_edge.vertex2
                        elif len(free_edges) is 0:
                            break
                    for edge, ch in list(road.items())[::-1]:
                        if ch is "random" and edge.vertex2 != vert1:
                            old_way.append(edge)
                            if not edge.oriented:
                                old_way.append(self.get_edge(edge.vertex2, edge.vertex1))
                            break
                    if vert1 in vert_with_min_edges[vert_with_min_edges.index(vert) + 1:]:
                        if str(vert) + str(vert1) in list(roads.keys()):
                            if len(list(road.keys())) < len(roads[str(vert) + str(vert1)]):
                                roads[str(vert) + str(vert1)] = list(road.keys())
                        else:
                            roads.setdefault(str(vert) + str(vert1), list(road.keys()))
                        print("We found one road from " + str(vert.name) + " to " + str(vert1.name) + " in " + str(
                            len(road)) + " turns")
                    for vert2 in self.vertexes:
                        vert2.check = True
                        for edge in vert2.edges:
                            if edge not in old_way:
                                edge.check = True
            if not self.weighted:
                return min(len(i) for i in list(roads.values())), max(len(i) for i in list(roads.values()))
            else:
                min_road = min(len(i) for i in list(roads.values()))
                max_road = max(len(i) for i in list(roads.values()))
                min_weight = 0
                max_weight = 0
                for road in list(roads.values()):
                    if min_weight != 0 and max_weight != 0:
                        break
                    if min_weight == 0 and len(road) == min_road:
                        for edge in road:
                            min_weight += edge.weight
                    if max_weight == 0 and len(road) == max_road:
                        for edge in road:
                            max_weight += edge.weight
                return min_weight, max_weight
        else:
            return 0, 0


class Vertex:
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name
        self.edges = []
        self.check = True

    def set_name(self, name):
        self.name = name


class Edge:
    def __init__(self, vertex1, vertex2, oriented):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.oriented = oriented
        self.weight = int()
        self.check = True

    def set_weight(self, weight):
        self.weight = weight
