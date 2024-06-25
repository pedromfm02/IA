
# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self, state, parent,  depth=0, cost=0, heuristic=0,action=None): 
        self.state = state
        self.parent = parent
        self.depth = depth #ex2 adiciona a possibilidade de calcular a depth a que está
        self.cost = cost #ex8 possibilita a habilidade de guardar o custo 
        self.heuristic = heuristic #ex12 possibilita a habilidade de guardar o valor da heuristica
        self.action = action #ex2 Strips guarda as açoes que foram feitas

    #previne ciclos na arvore de pequisa ex1
    def in_parent(self,newstate):
        if self.parent == None:
            return False
        if self.parent.state == newstate:
            return True
        return self.parent.in_parent(newstate)
        
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.non_terminals = 0 # ex5 definição da variavel que conta os nos n terminais
        self.highest_cost_nodes = [root] #ex15 guarda a lista com os nós com maior custo acumulado
        self._total_depth = 0 #ex16 guarda a depth total
        self.average_depth = 0 #ex16 guarda a avg depth dos nós 

    @property #ex5 calcula o numero de nodes terminais
    def terminals(self):
        return len(self.open_nodes ) +1

    @property #ex3
    def length(self):
        return self.solution.depth
    
    @property #ex6
    def avg_branching(self):
        return (self.terminals + self.non_terminals -1
                #todos os nós com excepção da raiz da árvore
                ) / self.non_terminals
                # a dividir por tds os nós nao terminais
    #EX9   
    @property
    def cost(self):
        return self.solution.cost

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)
    
    def get_operations(self, node):
        if node.parent == None:
            return []
        operations = self.get_operations(node.parent)
        operations += [node.action]
        return operations

    # procurar a solucao
    def search(self,limit=None):#ex4 funcionalidade de definir limite de profundidade na pesquisa
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.solution = node
                self.average_depth = self._total_depth / (self.terminals + self.non_terminals -1) #ex16 calcula a profundidade media dos nós
                self.plan = self.get_operations(node)
                return self.get_path(node)
            self.non_terminals += 1 #ex5 os nos nao terminais sao aqui adicionados
            lnewnodes = []
            for action in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,action)
                if (not node.in_parent(newstate)) and (#se o node ja for pai nao faz isto
                    limit == None or node.depth<limit): #ex4 funcionalidade de definir limite de profundidade na pesquisa
                    
                    newnode = SearchNode(newstate,
                                         node,
                                         node.depth+1, #ex2 adiciona a possibilidade de calcular a depth a que está
                                         node.cost + self.problem.domain.cost(node.state,action), #ex8 armazena o cost
                                         self.problem.domain.heuristic(newstate,self.problem.goal),#ex12 armazena a heuristica
                                         action 
                                        ) 
                    lnewnodes.append(newnode)

                    
                    self._total_depth += newnode.depth #ex16 calcula a depth total 

                    #ex15 permit calcular e armazenar os nós com o maior custo acumulado
                    if newnode.cost > self.highest_cost_nodes[0].cost:
                        self.highest_cost_nodes = [newnode]
                    elif newnode.cost == self.highest_cost_nodes[0].cost:
                        self.highest_cost_nodes.append(newnode)

            self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform': #ex10
            self.open_nodes.extend(lnewnodes) #adiciona a lista dos nos novos
            self.open_nodes.sort(key=lambda node: node.cost) #ordena essa lista tendo em conta o custo 
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes) #adiciona a lista dos nos novos
            self.open_nodes.sort(key=lambda node: node.heuristic) #ordena essa lista tendo em conta a heuristica 
        elif self.strategy == 'a*':  # junta os metodos de pesquisa uniforme e greedy
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda node: node.cost + node.heuristic)
