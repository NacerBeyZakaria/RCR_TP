% =============================================================
%  Série TP N° 2 - Base de connaissances : famille.pl
%  parent(X, Y) : X est un parent de Y
% =============================================================

homme(ali).  homme(omar).  homme(karim).  homme(yacine).  homme(rami).
femme(fatima).  femme(leila).  femme(sara).  femme(nour).  femme(ines).

parent(ali, omar).      parent(fatima, omar).
parent(ali, leila).     parent(fatima, leila).
parent(omar, yacine).   parent(sara, yacine).
parent(omar, nour).     parent(sara, nour).
parent(leila, rami).    parent(karim, rami).
parent(leila, ines).    parent(karim, ines).

pere(X, Y) :- parent(X, Y), homme(X).
mere(X, Y) :- parent(X, Y), femme(X).
grand_parent(X, Z) :- parent(X, Y), parent(Y, Z).
ancetre(X, Y) :- parent(X, Y). % cas de base
ancetre(X, Y) :- parent(X, Z), ancetre(Z, Y). % cas récursif

frere_soeur(X,Y) :- parent(Z,X) , parent(Z,Y) , X \= Y.
oncle(X,Y) :- (parent(P ,Y) , frere_soeur(X , P)) , homme(X).
cousin(X,Y) :- parent(P1 ,X) , parent(P2,Y) ,frere_soeur(P1,P2).

ancetre_bis(X, Y) :- ancetre_bis(Z, Y), parent(X, Z).
ancetre_bis(X, Y) :- parent(X, Y).
