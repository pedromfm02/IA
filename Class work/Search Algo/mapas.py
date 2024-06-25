from constraintsearch import *

region = ['A', 'B', 'C', 'D', 'E']
colors = ['red', 'blue', 'green', 'yellow', 'white']

mapa_a = {
    "A": "BED",
    "B": "AEC",
    "C": "BED",
    "D": "AEC",
    "E": "ABCD",
}

def make_constraint_graph(mapa):
    return { (x,y): lambda r1,c1,r2,c2: c1!=c2 for x in mapa for y in mapa[x]}

def make_domain(regions, colors):
    return { r:colors for r in regions}

cs = ConstraintSearch(None, None)

print(cs.search())
