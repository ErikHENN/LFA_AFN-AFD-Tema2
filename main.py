import pandas as pd

class Muchie:
    def __init__(self, legatura, litera):
        self.legatura = legatura
        self.litera = litera

class Nod:
    def __init__(self, eticheta, stare, nrm, Muchie):
        self.eticheta = eticheta
        self.stare = stare
        self.nrm = nrm
        self.Muchie = Muchie
class Automat:
    nr_noduri = int
    def __init__(self, alfabet, lista_noduri = []):
        self.alfabet = alfabet
        self.lista_noduri = lista_noduri
    def adauga_nod(self, nod):
        self.lista_noduri.append(nod)

def citire_automat(AFN):
    global nrn
    nrn = file.readline().rstrip("\n")
    for i in range(int(nrn)):
        legatura = []
        litera = []
        eticheta = i
        # stare =  ("Stare nod i")
        stare = file.readline().rstrip("\n")
        # nrm =  ("Nr. de legaturi ale nodului i"
        nrm = file.readline().rstrip("\n")
        for j in range(int(nrm)):
            # leg.append = "ID nod cu care se leaga nodul i"
            legatura.append(file.readline().rstrip("\n"))
            # lit.append="Litera acceptata pe legatura [i, leg[j]]"
            litera.append(file.readline().rstrip("\n"))
        M = Muchie(legatura, litera)
        N = Nod(eticheta, stare, nrm, M)
        AFN.adauga_nod(N)
    AFN.nr_noduri = len(AFN.lista_noduri)
    '''stari = [] #initializez o lista si o folosesc pe post de coada
    nod = 0 #nodul de unde pornesc
    noduri_vizitate = [False] * nrn

    while AFN:
        nod_final = False
        Nod_Curent = AFN[0]
        AFN.pop(-1)
        if Nod_Curent:
            AFD.append(Nod_Curent)
        for i in range(Nod_Curent.nrm):
            if AFN
'''


def listaNoduriPeLitera(litera, nod = Nod):
    lista = []
    indexNod = 0
    for c in nod.Muchie.litera:
        if c is litera:
            lista.append(nod.Muchie.legatura[indexNod])
        indexNod = indexNod + 1
    return lista


def creeazaTabelAutomat(AFN = Automat):
    lista_noduri = []
    for i in range(AFN.nr_noduri):
        lista_noduri.append(i)
    table = pd.DataFrame(index = lista_noduri, columns = list(AFN.alfabet) )
    for nod in lista_noduri:
        for litera in list(AFN.alfabet):
            if table[litera][nod]:
                table[litera][nod] = listaNoduriPeLitera(litera, AFN.lista_noduri[nod])
            else:
                table[litera][nod] = table[litera][nod] + listaNoduriPeLitera(litera, AFN.lista_noduri[nod])
    return table


def reunesteListe(lista1, lista2):
    return list(set().union(lista1, lista2))


'''
# Functia main
# 1) Deschid fisierul afd.in
# 2) Apelez functia de citire automat
# 3) Stochez cuvantul de verificat
# 4) Apelez functia de verificare cuvant 
'''


if __name__ == "__main__":
    file = open("afn.in", "r")
    AFN = Automat("abc")
    AFD = []
    citire_automat(AFN)
