from sympy import symbols, And, Or, Not, Equivalent
from sympy.logic.inference import satisfiable
from sympy.logic.boolalg import to_cnf
import itertools, time
from pysat.formula import CNF
from pysat.solvers import Solver

p, q, r = symbols('p q r')
f = (p >> q) & ~r
print(f) # affiche la formule
print(f.atoms()) # affiche les variables de la formule : {p, q, r}

f1 = p | ~p
f2 = p & ~p
f3 = (p >> q) & p

print(f1)
print(f2)
print(f3)

def table_verite(f):
 variables = sorted(f.atoms(), key=str)
 print(*variables, "|", f)
 for valeurs in itertools.product([True, False], repeat=len(variables)):
    interpretation = dict(zip(variables, valeurs))
    resultat = f.subs(interpretation) # valeur de f pour cette ligne
    print(*[int(v) for v in valeurs], "|", int(bool(resultat)))

table_verite(p >> q)

table_verite(f1)
table_verite(f2) 
table_verite(f3)

table_verite(((p >> q) & p) >> q)

print(satisfiable(p & q)) # un modèle : {p: True, q: True}
print(satisfiable(p & ~p)) # False : aucun modèle
print(list(satisfiable(p | q, all_models=True))) # tous les modèles de p | q

def est_satisfiable(f):
 return satisfiable(f) != False
def est_valide(f):
 return satisfiable(~f) == False # f est valide si non f n'a aucun modèle

print(satisfiable(((p >> q) & p) >> q))
print(satisfiable(((p >> q) & q) >> p))
print(satisfiable(p & ~p))

print(est_valide(((p >> q) & p) >> q))
print(est_valide(((p >> q) & q) >> p))
print(est_valide(p & ~p))

print(5*"\n")

print(est_valide(Equivalent(~(p & q) , ~p | ~q)))
print(est_valide(Equivalent(p >> q ,~q >> ~p )))
print(est_valide(Equivalent(p >> q , q >> p )))

BC = ["Si il pleut", "le match est annulé" , "Si le match est annulé" , "Ali reste à la maison", "Si Ali reste à la maison", "il étudie ou il dort" , "Ali ne dort pas. Il pleut"]

def decoule(BC, phi):
 base = And(*BC) #On regroupe toutes les formules de BC en une seule conjonction
 base_plus_non_phi = base & ~phi
 modele = satisfiable(base_plus_non_phi) # 3. On cherche un modèle de "BC et non phi"
 if modele == False:
 # Aucun modèle : BC et non phi est impossible,donc phi est vraie dans tous les modèles de BC
    return True
 else:
 # Il existe un modèle où BC est vraie et phi est fausse :
    print("Contre-exemple :", modele)
    return False


print(to_cnf(r >> q)) # ~r | q
print(to_cnf(r >> (p | q))) # p | q | ~r
print(to_cnf(p >> (q & r))) # (q | ~p) & (r | ~p)

base = CNF(from_file="test.cnf")
s = Solver(name='g3', bootstrap_with=base.clauses)
print(s.solve()) # True = SAT, False = UNSAT
print(s.get_model()) # un modèle, par exemple [1, -2, -3, -4, -5]
print(list(s.enum_models())) # tous les modèles