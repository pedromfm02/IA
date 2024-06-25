#encoding: utf8

# YOUR NAME: Pedro Matos
# YOUR NUMBER:102993

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT (names, numbers):
# - ...
# - ...

from semantic_network import *
from constraintsearch import *

class MySN(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)
        # ADD CODE HERE IF NEEDED
        self.assoc_stats = {}
        self.query_result = []
        pass

    def query_local(self,user=None,e1=None,rel=None,e2=None):
        declarations_class = [] #inicialização da variavel que guarda as declarações como objetos da classe declarations 

        # Este for, retira toda a informação do self.declarations que está em dicionário de dicionários,
        # E vai colocar essa informação no declaration_class na forma de objetos da classe declarations
        for user_key, decl_value in self.declarations.items():
            for (e1_key, rel_key), ents2 in decl_value.items():
                if isinstance(ents2, str): # Aqui é verificado se a relação do par (e1,rel) não é do tipo ASSOCIATION
                    declarations_class.append(self.make_decl(e1=e1_key, user=user_key, e2=ents2, rel=rel_key,rel_assoc = False))# Cria a declaration de acordo com a informação obtida
                else:#Aqui são geridas as e2 das relações tipo= ASSOCIATION
                    for e2_key in ents2:
                        declarations_class.append(self.make_decl(e1=e1_key, user=user_key, e2=e2_key, rel=rel_key))# Cria a declaration de acordo com a informação obtida

        # Em baixo faço o processamento do query_local para devolver o que é esperado
        self.query_result = [
            d for d in declarations_class
            if ((user is None or d.user == user)
                and (e1 is None or d.relation.entity1 == e1)
                and (rel is None or d.relation.name == rel)
                and (e2 is None or d.relation.entity2 == e2))
        ]
        
        return self.query_result # Your code must leave the output in
                          # self.query_result, which is returned here

    def query(self,entity,assoc=None):
        decl = self.query_local(e1=entity, rel= assoc) #vai buscar todas as declarações da entity com relação = assoc

        pred = [d.relation.entity2 for d in self.query_local(e1=entity) if isinstance(d.relation, (Member,Subtype))] # vai buscar todas as entidades que sao tipo ou super da entity

        #Neste for são adicionadas todas as declarações com relação = assoc das entidates ascendestes á entity 
        for p in pred:
            decl += self.query(p, assoc)

        self.query_result = [d for d in decl if isinstance(d.relation,(Association,AssocOne))] #Aqui o decl é filtrado para apenas devolver as declarações com relações do tipo, ASSOCIATION e ASSOCONE 

        return self.query_result # Your code must leave the output in
                          # self.query_result, which is returned here


    def update_assoc_stats(self,assoc,user=None):
    
        decl = self.query_local(rel=assoc,user=user)#devolve todas as declarações do user com relação=assoc 

        ent1 = [d.relation.entity1 for d in decl if (d.relation.entity1[0].isupper())]#guarda apenas as entidades 1 que são objetos
        ent2 = [d.relation.entity2 for d in decl if (d.relation.entity2[0].isupper())]#guarda apenas as entidades 2 que são objetos

        ent1_type = {} # guarda o nº de ocurrencias dos tipos que sao ascendentes aos objetos da lista ent1
        k1 = 0 # var que guarda o nº de objetos que não teem tipo na lista ent1
        #Neste for é calculado o nºde ocurrencias dos tipos que sao ascendentes aos objetos da lista ent1
        for e1 in ent1:
            types_e1 = self.query_type(e1,user)
            if not types_e1:#senão tiver tipo ascendente
                k1 += 1
            for typ_e1 in types_e1:
                if typ_e1 in ent1_type:
                    ent1_type[typ_e1] += 1
                else:
                    ent1_type[typ_e1] = 1

        ent2_type = {}# guarda o nº de ocurrencias dos tipos que sao ascendentes aos objetos da lista ent2
        k2 = 0 # var que guarda o nº de objetos que não teem tipo na lista ent2
        for e2 in ent2:
            #Neste for é calculado o nºde ocurrencias dos tipos que sao ascendentes aos objetos da lista ent1
            types_e2 = self.query_type(e2,user)
            if not types_e2: #senão tiver tipo ascendente
                k2 += 1
            for typ_e2 in types_e2:
                if typ_e2 in ent2_type:
                    ent2_type[typ_e2] += 1
                else:
                    ent2_type[typ_e2] = 1

        n = len(ent1) #nº de ocurrencias dos objetos
        
        #Neste for é calculada a frequencia relativa para cada tipo ascendete ás entidades da lista ent1
        for key_ent1,value_ent1 in ent1_type.items():
            div = n-k1+k1**(1/2)
            ent1_type[key_ent1] = value_ent1/div
        #Neste for é calculada a frequencia relativa para cada tipo ascendete ás entidades da lista ent2
        for key_ent2,value_ent2 in ent2_type.items():
            div = n-k2+k2**(1/2)
            ent2_type[key_ent2] = value_ent2/div

        self.assoc_stats[(assoc,user)] = (ent1_type,ent2_type) # guarda o resultado final na forma {(assoc,user):({stats assoc e1,stats assoc e2)}
        return self.assoc_stats
    
    def query_type(self,e1,user): # esta função auxiliar devolve todos os tipos ascendentes do e1 que o user declarou 
        types = set()
        entities = [d.relation.entity2 for d in self.query_local(e1=e1, user=user) if isinstance(d.relation, (Member,Subtype))] # devolve os nomes dos tipos ascendetes de e1
        types.update(entities)

        for ent in entities: #tendo em conta os tipos ascendentes de e1 guardados em entities vai buscar os tipos ascendentes desses tipos 
            types.update(self.query_type(ent, user))

        return types
    
    def make_decl(self,user,e1,rel,e2, rel_assoc= True): # esta função auxiliar devole o objeto Declaration de acordo com os argumentos
        if rel_assoc:
            return Declaration(user,Association(e1,rel,e2))
        else:
            if rel == 'subtype':
                return Declaration(user,Subtype(e1,e2))
            elif rel == 'member':
                return Declaration(user,Member(e1,e2))
            else:
                return Declaration(user,AssocOne(e1,rel,e2))    
                    

class MyCS(ConstraintSearch):

    def __init__(self,domains,constraints):
        ConstraintSearch.__init__(self,domains,constraints)
        # ADD CODE HERE IF NEEDED
        pass

    def search_all(self,domains=None,xpto=None):
        # If needed, you can use argument 'xpto'
        # to pass information to the function
        #
        # IMPLEMENTAR AQUI
        pass

