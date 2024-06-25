import asyncio
import json
import math
import websockets
import os
import getpass

# Define DigDug Search Domain
class DigDugSearchDomain():

    def __init__(self,state,fygar_range):
        self.enemies = state["enemies"]
        self.rocks = state["rocks"]
        self.digdug = state["digdug"]
        self.fygar_range = fygar_range

    def actions(self, coords):
        actlist = ["a", "s", "w", "d"]

        if coords[0] == 0:
            actlist.remove("a")

        if coords[1] == 0:
            actlist.remove("w")

        if coords[1] == 23:
            actlist.remove("s")

        if coords[0] == 47:
            actlist.remove("d")

        for rocks in self.rocks:
            if rocks["pos"][0]  == coords[0]: # se a pedra ta na mm coluna
                if  rocks["pos"][1] - 1 == coords[1]: # pedra em cima do digdug
                    actlist = ver_lista(actlist,"w")
                    actlist = ver_lista(actlist,"s")

                elif rocks["pos"][1] + 1 == coords[1]: # pedra em baixo do digdug
                    actlist = ver_lista(actlist,"s")

            if rocks["pos"][1]  == coords[1]: # se a pedra ta na mm linha
                if  rocks["pos"][0] - 1 == coords[0]: # pedra ta a direita do digdug
                    actlist = ver_lista(actlist,"a")

                elif rocks["pos"][0] + 1 == coords[0]: # pedra ta a esquerda do digdug
                    actlist = ver_lista(actlist,"d")
        
        # no caso de o dig dug estar atrás de um fygar           
        if self.fygar_range != []:
            for range_coords in self.fygar_range:
                if range_coords[0]  == coords[0]: # se o fygar ta na mm coluna
                    if  range_coords[1] - 1 == coords[1]: # fygar em cima do digdug
                        actlist = ver_lista(actlist,"w")

                    elif range_coords[1] + 1 == coords[1]: # fygar em baixo do digdug
                       actlist = ver_lista(actlist,"s")

                if range_coords[1]  == coords[1]: # se a fygar ta na mm linha
                    if  range_coords[0] - 1 == coords[0]: # fygar ta a direita do digdug
                        actlist = ver_lista(actlist,"a")

                    elif range_coords[0] + 1 == coords[0]: # fygar ta a esquerda do digdug
                        actlist = ver_lista(actlist,"d")
        return actlist 
        
    def result(self,coords,action):
        (x,y) = coords
        if action == "w":
            y -= 1
        elif action == "s":
            y += 1
        elif action == "a":
            x -= 1
        elif action == "d":
            x += 1

        return (x,y)
            
    def heuristic(self, coords, closest_enemy):
        #distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        distance = math.dist(coords, closest_enemy)
        return distance
            
    def satisfies(self, coords, closest_enemy):
        distance = math.dist(coords, closest_enemy)
        if distance == 0:
            return True
        return False

# define o Search Problem
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self, state, parent, action = "", heuristic=0): 
        self.state = state
        self.action = action
        self.parent = parent
        self.heuristic = heuristic 

    #previne ciclos na arvore de pequisa 
    def in_parent(self,newstate):
        if self.parent == None:
            return False
        if self.state == newstate:
            return True
        return self.parent.in_parent(newstate)
        
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem): 
        self.problem = problem
        root = SearchNode(problem.initial, None)
        self.open_nodes = [root]
        self.solution = None

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)
    
    # obter o caminho (sequencia de açoes) da raiz ate um no
    def get_path_ac(self,node):
        if node.parent == None:
            return [node.action]
        path = self.get_path_ac(node.parent)
        path += [node.action]
        return(path)

    # procurar a solucao
    def search(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.solution = node
                return self.get_path_ac(node),self.get_path(node)
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if (not node.in_parent(newstate)):
                    newnode = SearchNode(newstate,node,a,self.problem.domain.heuristic(newstate,self.problem.goal)) #ex12 armazena a heuristica 
                    lnewnodes.append(newnode)
            
            #estrategia de pesquisa: pesquisa gulosa
            self.open_nodes.extend(lnewnodes) #adiciona a lista dos nos novos
            self.open_nodes.sort(key=lambda node: node.heuristic) #ordena essa lista tendo em conta a heuristica 
        
        return None

#-------------------------------------- Agente ------------------------------------------
async def agent_loop(server_address="localhost:8000", agent_name="student"):
    # Create an instance of DigDugSearchDomain
    async with websockets.connect(f"ws://{server_address}/player") as websocket:
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        while True:
            try:
                state = json.loads(await websocket.recv())

                if "map" in state:
                    map = state["map"] # guarda o novo mapa quando o jogador primeiro se connecta ou qd muda de nivel
                    dir_dig = 1
                    enemy = {'name':"",'pos': [0,0], 'dir':0, 'id': ''} # aqui é guardada a informação do inimigo que o dig dug está a ir atrás

                if "digdug" in state and "enemies" in state:
                    digdug_pos = state["digdug"]
                    enemies = state["enemies"]
                    rocks = state["rocks"]
                    

                    if enemies:
                        closest_enemy = min(enemies, key=lambda enemy: abs(digdug_pos[0] - enemy["pos"][0]) + abs(digdug_pos[1] - enemy["pos"][1])) # calcula o inimigo mais próximo
                        initial_state = digdug_pos
                        
                        # aqui é verificado se o inimigo é o msm q estava anteriormente guardado
                        # se for o msm calcula a sua direção se houver movimento por parte do inimigo
                        # se não for o msm guarda a nova informação
                        if enemy["id"] == closest_enemy["id"]:
                            if enemy["pos"] != closest_enemy["pos"]:
                                if enemy["pos"][0] == closest_enemy["pos"][0]:
                                    if enemy["pos"][1] > closest_enemy["pos"][1]:
                                        enemy["dir"] = 0
                                    else:
                                        enemy["dir"] = 2
                                else:
                                    if enemy["pos"][0] > closest_enemy["pos"][0]:
                                        enemy["dir"] = 3
                                    else:
                                        enemy["dir"] = 1
                        else:
                            enemy["id"] = closest_enemy["id"]
                            enemy["name"] = closest_enemy["name"]
                            enemy["dir"] = closest_enemy["dir"]
                        
                        enemy["pos"] = closest_enemy["pos"]

                        fygar_range = [] # guarda as coordenadas, do possivel fogo do fygar
                        if enemy["name"] == "Fygar":
                            for dist in [-1,-2,-3,-4]:
                                fygar_range.append(calc_coords(enemy["dir"],enemy["pos"],dist))

                        s = DigDugSearchDomain(state,fygar_range) #é definido o search domain tendo em conta a informação do state e o range do fygar
                        
                        #goalstate modificado para o digdug aparecer atrás do inim com dist 3
                        goal_state = calc_coords(enemy["dir"],enemy["pos"],3)
                        
                        #verifica se o inimigo mais proximo está a uma distancia menor ao igual a 2 ou 3
                        dist = math.dist(initial_state, enemy["pos"])
                        
                        if dist <= 3: # este if serve para saber se o digdug está em posição de ataque ou não
                            #verifica se o dig dug está numa possição aceitavel para atacar e devolve a ação para o digdug se posicionar para atacar
                            ver,a = ver_coords(enemy["dir"],initial_state,enemy["pos"],map)
                            if ver and not kill:
                                dir_dig = ver_dir_dig_dug(a)
                                kill = True
                                await websocket.send(
                                        json.dumps({"cmd": "key", "key": a})
                                    )
                            else:
                                x,y = calc_coords(dir_dig,initial_state,-1)
                                if map[x][y] == 0: 
                                    if ver_rocks(rocks,initial_state): 
                                        await websocket.send(
                                                json.dumps({"cmd": "key", "key": "AB"})
                                            )
                                    else:
                                        if dir_dig == 1:
                                            action = "a"
                                        elif dir_dig == 2:
                                            action = "a" 
                                        elif dir_dig == 3:
                                            action = "d"
                                        else:
                                            action = "d"
                                        
                                        await websocket.send(
                                                json.dumps({"cmd": "key", "key": action})
                                            )
                                else:
                                    kill = False
                        else:
                            # aqui é aplicada a search tree para calcular o mlhr caminho para o objetivo definido em cima
                            kill = False
                            problem = SearchProblem(s, initial_state, goal_state)
                            tree = SearchTree(problem)
                            path,coord = tree.search()
                            
                            if path: 
                                if len(path) != 1: 
                                    update_map(map,coord[1]) # dá update do mapa para saber que espaços é que estão vazios ou ainda com terreno 
                                    dir_dig = ver_dir_dig_dug(path[1])                     
                                    await websocket.send(
                                        json.dumps({"cmd": "key", "key": path[1]})
                                    )                     
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return
            
#---------------------funçoes auxiliares---------------------------------
def ver_coords(dir, dig_dug, enemy,map): # verifica as coordenadas do dig_dug se td estiver como o esperado devolve True e a ação a praticar
    x,y = enemy
    if map[x][y] == 0: # aqui verifica se o inimigo está ou não em espaço aberto
        if dir == 0 or dir == 2: # verifica se o inimigo se está a movimentar no eixo vertical
            if dig_dug[0] == enemy[0]: 
                if dir == 0: 
                    if dig_dug[1] < enemy[1]:
                        return True,"d"
                    return True,"w"
                else:
                    if dig_dug[1] > enemy[1]:
                        return True,"a"
                    return True,"s"
        else:
            if dig_dug[1] == enemy[1]:
                if dir == 1:
                    if dig_dug[0] > enemy[0]:
                        return True, "w"
                    return True,"d"
                else:
                    if dig_dug[0] < enemy[0]:
                        return True, "s"
                    return True,"a"
    return False,""

def update_map(map, coord): # dá update ao mapa opós o dig dug se movimentar
    x,y = coord
    map[x][y] = 0

def calc_coords(dir, coord, dist): #«calcula as coordenadas desejadas tendo em conta a direção e a distancia pretendida
    goal_coord = [0,0]
    if dir == 0 : # dir cima 
        goal_coord[0] = coord[0]
        goal_coord[1] = abs(coord[1] + dist)
    elif dir == 2:# dir baixo 
        goal_coord[0] = coord[0]
        goal_coord[1] = abs(coord[1] - dist) 
    elif dir == 1:# dir direita
        goal_coord[1] = coord[1]
        goal_coord[0] = abs(coord[0] - dist) 
    else: # dir esq
        goal_coord[1] = coord[1]
        goal_coord[0] = abs(coord[0] + dist)
    
    #verifica se o goal_coord tem coordenadas aceitaveis
    if goal_coord[0] > 47:
        goal_coord[0] = 47
    if goal_coord[1] > 23:
        goal_coord[1] = 23
    
    return goal_coord

def ver_dir_dig_dug(action): # devolve a dir em q o dig_dug está tendo em conta a ação que tomou
    if action == "w":
        return 0
    if action == "a":
        return 3
    if action == "d":
        return 1
    if action == "s":
        return 2

def ver_rocks(rocks,dig_dug): #verifica se existe alguma pedra em cima do dig dug
    coord_cima = calc_coords(0,dig_dug,-1)
    for rock in rocks:
        if coord_cima == rock["pos"]:
            return False
    return True

def ver_lista(act_list, action): #esta função permite a eliminação de dados dentro de uma lista sem correr o risco de dar erro
    if action in act_list:
        act_list.remove(action)
    return act_list

#DO NOT CHANGE THE LINES BELOW
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
