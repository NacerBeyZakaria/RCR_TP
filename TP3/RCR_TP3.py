import itertools
import networkx as nx
import matplotlib.pyplot as plt

mondes = {"w1", "w2", "w3", "w4", "w5"}
# (u, v) dans R : le monde v est accessible depuis le monde u
R = {("w1", "w2"), ("w1", "w3"), ("w2", "w2"), ("w3", "w4"),
 ("w4", "w1"), ("w4", "w5")}
# pour chaque variable, l'ensemble des mondes où elle est vraie
V = {"p": {"w2", "w3"}, "q": {"w2", "w4", "w5"}}
M = (mondes, R, V) # le modèle de Kripke

def successeurs(R, w): # mondes accessibles depuis w
 return {v for (u, v) in R if u == w}
for w in sorted(mondes):
 print(w, "->", sorted(successeurs(R, w)))

print(successeurs(R,mondes))

def dessiner(M, titre="Modèle de Kripke"):
 mondes, R, V = M
 G = nx.DiGraph()
 G.add_nodes_from(mondes)
 G.add_edges_from(R)
 # étiquette de chaque monde : son nom et les variables vraies
 etiq = {w: w + "\n" + ",".join(sorted(x for x in V if w in V[x]))
 for w in mondes}
 nx.draw(G, nx.circular_layout(G), labels=etiq, node_size=1800,
 node_color="lightblue", arrowsize=20, connectionstyle="arc3,rad=0.1")
 plt.margins(0.2) # laisse de la place aux étiquettes
 plt.title(titre)
 plt.show()
dessiner(M)

C = {"p": {"w2", "w3"}, "q": {"w2", "w4", "w5"}, "r": {"w1"}}
M2 = (mondes, R, C)

dessiner(M2)

def Non(f): return ("non", f)
def Et(f, g): return ("et", f, g)
def Ou(f, g): return ("ou", f, g)
def Imp(f, g): return ("imp", f, g)
def Nec(f): return ("nec", f) # □f : f est nécessaire
def Pos(f): return ("pos", f) # ◇f : f est possible

def vrai(M, w, f): # M, w ⊨ f ?
 mondes, R, V = M
 if isinstance(f, str): # variable propositionnelle
    return w in V.get(f, set())
 op = f[0]
 if op == "non": return not vrai(M, w, f[1])
 if op == "et": return vrai(M, w, f[1]) and vrai(M, w, f[2])
 if op == "ou": return vrai(M, w, f[1]) or vrai(M, w, f[2])
 if op == "imp": return (not vrai(M, w, f[1])) or vrai(M, w, f[2])
 if op == "nec": return all(vrai(M, v, f[1]) for v in successeurs(R, w))
 if op == "pos": return any(vrai(M, v, f[1]) for v in successeurs(R, w))
 raise ValueError("opérateur inconnu : " + op)

def afficher(f): # écriture lisible d'une formule
 if isinstance(f, str): return f
 un = {"non": "¬", "nec": "□", "pos": "◇"}
 if f[0] in un: return un[f[0]] + afficher(f[1])
 bin_ = {"et": " ∧ ", "ou": " ∨ ", "imp": " → "}
 return "(" + afficher(f[1]) + bin_[f[0]] + afficher(f[2]) + ")"
def table_mondes(M, f): # valeur de f dans chaque monde
 print(afficher(f), ":", {w: int(vrai(M, w, f)) for w in sorted(M[0])})

table_mondes(M, "p")
table_mondes(M, Nec("p")) # □p
table_mondes(M, Pos("p")) # ◇p
table_mondes(M, Nec(Ou("p", "q"))) # □(p ∨ q)

table_mondes(M, Pos("q"))
table_mondes(M, Nec(Nec("p")))
table_mondes(M, Pos(Nec("q")))
table_mondes(M, Imp(Pos("p"),"p"))
table_mondes(M, Imp(Nec("p"), Pos("p")))

# question 3:
table_mondes(M, Nec("p"))
table_mondes(M , Non(Pos(Non("p"))))
table_mondes(M, Pos("p")) 
table_mondes(M, Non(Nec(Non("p"))))

def valide_modele(M, f): # f est vraie dans TOUS les mondes de M
 return all(vrai(M, w, f) for w in M[0])

print(valide_modele(M, Imp(Nec("p") ,"p")))
print(valide_modele(M, Imp(Nec("p") , Pos("p"))))

def reflexive(W, R): return all((w, w) in R for w in W)
def symetrique(W, R): return all((v, u) in R for (u, v) in R)
def transitive(W, R):
 return all((u, x) in R for (u, v) in R for (y, x) in R if v == y)
def serielle(W,R): return all(any((w,v) in R for v in W) for w in W)
def euclidienne(W, R): return all((u , v) in R for (x , u) in R for (y , v) in R if x == y)
def proprietes(W, R):
 for nom, test in [("réflexive", reflexive), ("sérielle", serielle),
 ("symétrique", symetrique), ("transitive", transitive),
 ("euclidienne", euclidienne)]:
    print(f" {nom:12}: {test(W, R)}")

print(proprietes(M[0],M[1]))    

D = {("w1", "w2"), ("w1", "w3"), ("w2", "w2"), ("w3", "w4"),
 ("w4", "w1"), ("w4", "w5"), ("w5", "w5")}

M3 = (mondes ,D , V)
print(proprietes(M3[0],M3[1]))  


dessiner(M3)

# Les mondes sont les états d'un feu tricolore ; T relie un état au suivant
etats = {"s0", "s1", "s2", "s3"}
T = {("s0", "s1"), # rouge -> vert
 ("s1", "s2"), # vert -> orange
 ("s2", "s0"), ("s2", "s3"), # orange -> rouge, ou orange -> panne
 ("s3", "s3")} # en panne, le feu reste en panne
L = {"rouge": {"s0"}, "vert": {"s1"}, "orange": {"s2", "s3"}, "panne": {"s3"}}
FEU = (etats, T, L)

dessiner(FEU , "Fue tricolore")

def futur(R, w):
   """Tous les états atteignables depuis w en 0, 1, 2... étapes."""
   vus, a_visiter = {w}, [w]
   while a_visiter:
      u = a_visiter.pop()
      for v in successeurs(R, u):
         if v not in vus:
            vus.add(v)
            a_visiter.append(v)
   return vus
def fermeture(W, R): # la relation « w peut atteindre v »
   return {(w, v) for w in W for v in futur(R, w)}

def AX(f): return ("AX", f) # à l'état suivant, quel qu'il soit
def EX(f): return ("EX", f) # il existe un état suivant où f
def AG(f): return ("AG", f) # toujours, sur tous les chemins
def EF(f): return ("EF", f) # un jour, sur au moins un chemin
def EU(f, g): return ("EU", f, g) # un chemin où f reste vraie jusqu'à g

def vrai_t(M, w, f):
   W, R, V = M
   if isinstance(f, str):
      return w in V.get(f, set())
   op = f[0]
   if op == "non": return not vrai_t(M, w, f[1])
   if op == "et": return vrai_t(M, w, f[1]) and vrai_t(M, w, f[2])
   if op == "ou": return vrai_t(M, w, f[1]) or vrai_t(M, w, f[2])
   if op == "imp": return (not vrai_t(M, w, f[1])) or vrai_t(M, w, f[2])
   if op == "AX": return all(vrai_t(M, v, f[1]) for v in successeurs(R, w))
   if op == "EX": return any(vrai_t(M, v, f[1]) for v in successeurs(R, w))
   if op == "AG": return all(vrai_t(M, v, f[1]) for v in futur(R, w))
   if op == "EF": return any(vrai_t(M, v, f[1]) for v in futur(R, w))
   if op == "EU":
   # on avance tant que f est vraie, et on cherche un état où g est vraie
                  vus, a_visiter = set(), [w]
                  while a_visiter:
                     u = a_visiter.pop()
                     if vrai_t(M, u, f[2]):
                      return True
                  if u not in vus and vrai_t(M, u, f[1]):
                     vus.add(u)
                     a_visiter.extend(successeurs(R, u))
                  return False
   raise ValueError("opérateur inconnu : " + op)
            # valeur de la propriété f dans chaque état
def verifier(M, f, nom):
   print(f"{nom:32}", {w: int(vrai_t(M, w, f)) for w in sorted(M[0])})

for s in sorted(etats):
 print(s, "futur :", sorted(futur(T, s)))
verifier(FEU, AG(Non(Et("rouge", "vert"))), "P1 : AG ¬(rouge ∧ vert)")
verifier(FEU, EF("vert"), "P2 : EF vert")
verifier(FEU, AG(Imp("vert", AX("orange"))), "P3 : AG (vert → AX orange)")
verifier(FEU, AG(Imp("orange", AX("rouge"))), "P4 : AG (orange → AX rouge)")
verifier(FEU, AG(EF("rouge")), "P5 : AG EF rouge")
verifier(FEU, EU(Non("vert"), "panne"), "P6 : E[¬vert U panne]")

R_futur = fermeture(etats, T)
print("Propriétés de la relation « futur » :")
proprietes(etats, R_futur)
for a in ["T : □p → p", "4 : □p → □□p", "B : p → □◇p"]:
 print(f" {a:24} {valide_cadre(etats, R_futur, axiomes[a])}")