

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

from collections import Counter
from functools import reduce
from statistics import mean


class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)



#   Exemplo:
#   a = Association('socrates','professor','filosofia')

class AssocOne(Association):
    def __init__(self, e1, assoc, e2):
        Association.__init__(self,e1, assoc, e2)

class AssocNum(Association):
    def __init__(self, e1, assoc, e2):
        Association.__init__(self,e1, assoc, e2)

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return str(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel_type=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel_type == None or isinstance(d.relation, rel_type))
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    def list_associations(self): #EX1
        d = self.query_local(rel_type=Association)
        return list(set([decl.relation.name for decl in d]))
    
    def list_objects(self): #EX2
        d = self.query_local(rel_type=Member)
        return list(set([decl.relation.entity1 for decl in d]))
    
    def list_users(self): #EX3
        d = self.query_local()
        return list(set([decl.user for decl in d]))
    
    def list_types(self): #EX4
        d1 = self.query_local(rel_type=Subtype)
        d2 = self.query_local(rel_type=Member)
        return list(
            set(
                [decl.relation.entity1 for decl in d1] 
                + [decl.relation.entity2 for decl in d1+d2]
            )
        )
    
    def list_local_associations(self, entity): #EX5
        d1 = self.query_local(e1=entity, rel_type=Association)
        d2 = self.query_local(e2=entity, rel_type=Association)
        return list(
            set(
                [decl.relation.name for decl in d1+d2]
            )
        )
    
    def list_relations_by_user(self,user): #EX6
        d = self.query_local(user=user)
        return list(
            set(
                [decl.relation.name for decl in d]
            )
        )
    
    def associations_by_user(self, user): #EX7
        d1 = self.query_local(user=user,rel_type=Association)
        return len(
            list(
                set(
                    [decl.relation.name for decl in d1]
                )
            )
        )
    
    def list_local_associations_by_entity(self,entity): #EX8
        d1 = self.query_local(e1=entity,rel_type=Association)
        d2 = self.query_local(e2=entity,rel_type=Association)
        return list(
                set(
                    [(decl.relation.name,decl.user) for decl in d1+d2]
                )
            )
        
    def predecessor(self, a,b): #EX9
        d1 = self.query_local(e1=b,rel_type=(Subtype,Member))
       
        if d1 == []:
            return False
        
        if a in [decl.relation.entity2 for decl in d1]:
            return True
        
        return any([self.predecessor(a, decl.relation.entity2) for decl in d1])
    
    def predecessor_path(self, a, b): #EX 10
        decl = self.query_local(e1=b, rel_type=(Subtype,Member))

        if decl == []:
            return None
        
        if a in [d.relation.entity2 for d in decl]:
            return [a,b]
        
        for pred in [d.relation.entity2 for d in decl]:
            if res:= self.predecessor_path(a,pred): # ver o que é :=
                return res + [b]  
            
    def query(self, entity, rel=None): #EX 11 a)
        decl = self.query_local(e1=entity, rel=rel, rel_type=Association)

        pred = [d.relation.entity2 for d in self.query_local(e1=entity, rel_type=(Member,Subtype))]

        for p in pred:
            decl += self.query(p, rel)
        return decl
    
    def query2(self, entity, rel=None): #EX 11 b)
        decl = self.query_local(e1=entity, rel_type=(Member,Subtype))

        return decl + self.query(entity, rel)
    
    def query_cancel(self, entity, rel=None): #EX 12
        decl = self.query_local(e1=entity, rel=rel, rel_type=Association)

        pred = [d.relation.entity2 for d in self.query_local(e1=entity, rel_type=(Member,Subtype))]

        decl_name = [d.relation.name for d in decl]

        for p in pred:
            decl += [d for d in self.query_cancel(p,rel) if d.relation.name not in decl_name]

        return decl
    
    def query_down(self, entity, rel=None, first=True): #EX 13
        decl = [] if first else self.query_local(e1=entity, rel=rel, rel_type=Association)

        desc = [d.relation.entity1 for d in self.query_local(e2=entity, rel_type=(Member,Subtype))]

        for d in desc:
            decl += [decl for decl in self.query_down(d, rel, False)]

        return decl
    
    def query_induce(self, entity, rel): #EX 14
        decl = self.query_down(entity, rel)

        return Counter([d.relation.entity2 for d in decl]).most_common(1)[0][0]
    
    def query_local_assoc(self, entity, rel): #ex15
        local = self.query_local(e1=entity, rel=rel)

        for d in local:
            if isinstance(d.relation, AssocOne):
                val, count = Counter([d.relation.entity2 for d in local]).most_common(1)[0]
                return val , count/len(local)
            if isinstance(d.relation, AssocNum):
                return mean([d.relation.entity2 for d in local])
            if isinstance(d.relation, Association):
#mankings
                mc = []
                freq = 0
                for val, count in Counter([d.relation.entity2 for d in local]).most_common():
                    mc.append((val, count/len(local)))
                    freq += count/len(local)
                    if freq > 0.75:
                        return mc
#prof            
#                l = Counter([d.relation.entity2 for d in local]).most_common()

#                r = [(val, count/len(local)) for val,count in l]
#com reduce
#                def aux(carry, elem):
#                    l, lim = carry
#
#                    v,f = elem
#                    
#                    return (l+[v] , lim+f) if lim < 0.75 else 1
#
#                return reduce(aux, r, ([],0))
#com for
#                lim = 0
#                res = []
#                for v,f in r:
#                    lim += f
#                    res.append((v,f))
#                    if lim > 0.75:
#                        return res
#
#                return r
            
    def query_assoc_value(self, E, A):
        local = self.query_local(e1=E, rel=A)

        l_c = Counter([d.relation.entity2 for d in local]).most_common(1)

        if len(l_c) == 1:
            return l_c[0][0]
        
        herdados = self.query(entity=E, rel=A)
        h_c = Counter([d.relation.entity2 for d in herdados]).most_common()

        return h_c[0][0]
