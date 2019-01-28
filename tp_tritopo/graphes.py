#coding:utf-8

# ALGORITHMIQUE
# TP TRI TOPOLOGIQUE
# REPAIN Paul
# 2019

class Digraph:
    """Directed graph"""

    def __init__(self, adjacency):
        # adjacency is a dictionary
        # vertex -> list of vertices
        self.adjacency = adjacency

    def getListVertices(self):
        """returns list of vertices"""
        return self.adjacency.keys()

    def pprint(self):
        print "Vertices are :", self.getListVertices()
        for k in self.getListVertices():
            print "Outneighbours of", k, "are", self.adjacency[k]

    def getOrder(self):
        """returns number of vertices"""
        return len(self.adjacency)

    def getOutdegree(self, v):
        """returns the number of outneighbours of a vertex"""
        return len(self.adjacency[v])

    def getOutNeighbours(self, v):
        return self.adjacency[v]

    def getSize(self):
        """returns the number of arcs of a digraph"""
        return sum([self.getOutdegree(v) for v in self.adjacency])

    def topological_ordering(self):
        """returns a topological ordering of a graph, supposed to be a dag
        numerotation = vertex -> int"""
        counter = self.getOrder()
        toporder = {}

        for v in self.adjacency:
            toporder[v] = None

        # list of vertices not numbered/sorted
        notNumVertices = self.getListVertices()

        while notNumVertices:
            v = notNumVertices[0]
            # we seek a sink not numbered
            # while v has an outneighbour not numbered
            neigh_not_numb = [neigh for neigh in self.adjacency[v] if toporder[neigh] == None]

            while neigh_not_numb:
                v = neigh_not_numb[0]
                neigh_not_numb = [neigh for neigh in self.adjacency[v] if toporder[neigh] == None]
            notNumVertices.remove(v)
            toporder[v] = counter
            counter -= 1
        return toporder



    def verify_topological_ordering(self, toporder):
        """checks if the ordering given is a topological ordering
        if the rank of the out neighbour is lower, it is wrong
        else, true"""
        for v in self.getListVertices():
            for n in self.adjacency[v]:
                if toporder[n] < toporder[v]:
                    return False
        return True


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


