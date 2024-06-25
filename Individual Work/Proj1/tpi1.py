#STUDENT NAME: Pedro Matos
#STUDENT NUMBER: 102993

#DISCUSSED TPI-1 WITH: (names and numbers):


import math
from tree_search import *

class OrderDelivery(SearchDomain):

    def __init__(self,connections, coordinates):
        self.connections = connections
        self.coordinates = coordinates
        # ANY NEEDED CODE CAN BE ADDED HERE

    def actions(self,state):
        city = state[0]
        actlist = []
        for (C1,C2,D) in self.connections:
            if (C1==city):
                actlist += [(C1,C2)]
            elif (C2==city):
               actlist += [(C2,C1)]
        return actlist 

    def result(self,state,action):
        (city,targets) = state
        
        (C1,C2) = action
        if C1==city:
            if C2 in targets:
                lst = []
                for target_city in targets:
                    if  C2 != target_city:
                        lst.append(target_city)
                
                return(C2,lst)
            
            return (C2,targets)

    def satisfies(self, state, goal):
        city = state[0]
        if state[1] == []:
            return goal==city
        return False
    
    def cost(self, state, action):
        city = state[0]
        (C1, C2) = action
        if C1==city:
            for (x1, x2, d) in self.connections:
                if (x1, x2) in [(C1,C2),(C2,C1)]:
                    return d
                
    def heuristic(self, state, goal): # mudar heuristica
        (city,targets) = state
        if targets == []:
            c1_x, c1_y = self.coordinates[city]
            c2_x, c2_y = self.coordinates[goal]
            return round(math.hypot(c1_x - c2_x, c1_y - c2_y))
        total_dist = 0
        for target_city in targets:
            c1_x, c1_y = self.coordinates[city]
            c2_x, c2_y = self.coordinates[target_city]
            total_dist += round(math.hypot(c1_x - c2_x, c1_y - c2_y))
        return total_dist

 
class MyNode(SearchNode):

    def __init__(self,state,parent,depth=0,cost=0,heuristic=0,eval=0,deletion=False):
        super().__init__(state,parent)
        #ADD HERE ANY CODE YOU NEED
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.eval = eval   
        self.deletion = deletion

class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth',maxsize=None):
        super().__init__(problem,strategy)
        #ADD HERE ANY CODE YOU NEED
        self.maxsize = maxsize
        self.problem = problem
        root = MyNode(problem.initial, None)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.non_terminals = 0

    def astar_add_to_open(self,lnewnodes):
        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key=lambda node: (node.eval, node.state))

    def search2(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes)+1
                return self.get_path(node)
            self.non_terminals += 1
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if newstate not in self.get_path(node):
                    depth = node.depth + 1
                    cost = node.cost +self.problem.domain.cost(node.state,a)
                    heuristic = self.problem.domain.heuristic(newstate,self.problem.goal)
                    eval= cost + heuristic
                    newnode = MyNode(newstate,node,depth,cost,heuristic,eval)
                    lnewnodes.append(newnode)
            self.add_to_open(lnewnodes)
            
            if self.strategy == "A*" and self.maxsize != None:
                if self.maxsize < (len(self.open_nodes) + 1 + self.non_terminals): # este segmento não está a funcionar
                    self.manage_memory()   #inflizmente o manage_memory nao esta funcionar 
                

                
        return None

    def manage_memory(self):   
        for node in reversed(self.open_nodes):
            if not node.deletion:
                node.deletion = True
                
                children = self.check_children(node.parent) # função que verifica se os siblings estão marcados para eleminação
                if children != []:
                    n = node.parent
                    eval_min = 0
                    for child in children:
                        if eval_min > child.eval:
                            eval_min = child.eval
                        self.open_nodes.remove(child)                  
                    n.eval = eval_min
                    self.open_nodes.append(n)
                    tree_size = len(self.open_nodes) + 1 + self.non_terminals
                    if self.maxsize < tree_size:
                        self.manage_memory()
                    return True

    def check_children(self, parent):
        lst_children = []
        for node in reversed(self.open_nodes):
            if node.parent == parent:
                lst_children.append(node)

        for child in lst_children:
            if not child.deletion:
                lst_children = []
                return lst_children

        return lst_children

    # if needed, auxiliary methods can be added here
def orderdelivery_search(domain,city,targetcities,strategy='breadth',maxsize=None):
    
    p = SearchProblem(domain,(city,targetcities),city)
    t = MyTree(p,strategy,maxsize)
    
    path_not_clear = t.search2()

    path = []
    for state in path_not_clear:
        (city,targets) = state
        path.append(city)

    return t,path

# If needed, auxiliary functions can be added here



