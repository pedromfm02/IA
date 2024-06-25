from constraintsearch import *

amigos = ["Andre", "Bernardo", "Claudio"]

cs = ConstraintSearch(None, None)

def constraint(a1,i1,a2,i2):
    b1, c1 = i1
    b2, c2 = i2

    if a1 in i1 or a2 in i2: # nao posso levar as  minhas c oisas~
        return False
    
    if b1 == c1 or b2 == c2: # nao posso levar coisas do mesmo amigo
        return False
    
    if c1 == "Claudio" and b1 != "Bernardo":
        return False
    if c2 == "Claudio" and b2 != "Bernardo":
        return False
    return True

def make_constraint_graph(amigos):
    return { (x,y): constraint for x in amigos for y in amigos if x != y}

def make_domain(amigos):
    return { a: [(b,c) for b in amigos for c in amigos] for a in amigos}

cs = ConstraintSearch(make_domain(amigos), make_constraint_graph(amigos))
print(cs.search())
