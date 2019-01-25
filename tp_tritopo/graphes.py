#coding:utf-8

# ALGORITHMIQUE
# TP TRI TOPOLOGIQUE
# REPAIN Paul
# 2019

class Digraph:
    """Directed graph"""

    def __init__(self, adjacency):
        # adjacency is a dictionary
        # edge -> list of edges
        self.adjacency = adjacency

    def getListVertices(self):
        """returns list of vertices"""
        return self.adjacency.keys()

    def pprint(self):
        print "Vertices are :", self.getListVertices()
        for k in self.getListVertices():
            print "Exiting neighbours of", k, "are", self.adjacency[k]

    def getOrder(self):
        """returns number of vertices"""
        return len(self.adjacency)

    def getExitingDegree(self, v):
        """returns the number of exiting neighbours of a vertice"""
        return len(self.adjacency[v])

    def getSize(self):
        """returns the number of arcs of a digraph"""
        return sum([self.getExitingDegree(v) for v in self.adjacency])

    def topological_ordering(self):
        """returns a topological ordering of a graph, supposed to be a dag
        numerotation = vertice -> int"""
        counter = self.getOrder() - 1
        sort = {}

        for v in self.adjacency:
            sort[v] = None

        notNumVertices = self.getListVertices()

        while notNumVertices:
            v = notNumVertices.pop()
            # seek a sink not numbered
            neigh_not_numb = [neigh in self.adjacency[v] if sort[neigh] == None]
            while neigh_not_numb:
                v = neigh_not_numb[0]
                neigh_not_numb = [neigh in self.adjacency[v] if sort[neigh] == None]



    def verify_topological_ordering(self):
        """checks if the ordering given is a topological ordering"""


def readGraph(filename):
    """returns a graph read from a file"""
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    for l in lines:
        words = l.split()
        if len(words) >= 2 and words[0] == 'ordre':
            order = int(words[1])
            adj = {}
            for v in range(order):
                adj[v] = []

        if len(words) >= 3 and words[0] in ['A', 'E']:
            beginVertice = int(words[1])
            endVertice = int(words[2])
            adj[beginVertice].append(endVertice)

    return Digraph(adj)


