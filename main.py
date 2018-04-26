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
        lista_noduri.append(str(i))
    table = pd.DataFrame(index = lista_noduri, columns = list(AFN.alfabet + '@') )#@ reprezinta coloana in DATAFRAME pentru vizitat si o voi completa cu true / false
    #Generez nodurile initiale din AFN
    for nod in lista_noduri:
        for litera in list(AFN.alfabet):
            if table[litera][nod]:
                table[litera][nod] = listaNoduriPeLitera(litera, AFN.lista_noduri[int(nod)])
            else:
                table[litera][nod] = table[litera][nod] + listaNoduriPeLitera(litera, AFN.lista_noduri[int(nod)])
    #Marchez toate nodurile ca nevizitate
    for nod in lista_noduri:
        table['@'][nod] = False
    #Generez nodurile combinate
    for litera in list(AFN.alfabet):
        for nod in lista_noduri:
            tranzitie_noua = []
            lista_de_tranzitii = table[litera][nod]
            if (type(lista_de_tranzitii) is list and len(lista_de_tranzitii) > 1) and table['@'][nod] is False:
                for tranzitie in lista_de_tranzitii:
                    for c in tranzitie:
                        tranzitie_noua = reunesteListe(tranzitie_noua, table[litera][c])
                eticheta_tranzitie_noua = ''.join(lista_de_tranzitii)
                lista_noduri.append(eticheta_tranzitie_noua)
                table.loc[eticheta_tranzitie_noua] = False
                table.loc[eticheta_tranzitie_noua][litera] = tranzitie_noua
                print(table)
    return table


def reunesteListe(lista1, lista2):
    return list(set().union(lista1, lista2))

def creeazaTranzitiiNoi(AFN = Automat):
    lista = []


'''
# Functia main
# 1) Deschid fisierul afd.in
# 2) Apelez functia de citire automat
# 3) Stochez cuvantul de verificat
# 4) Apelez functia de verificare cuvant 
'''


if __name__ == "__main__":
    file = open("afn.in", "r")
    AFN = Automat("ab")
    AFD = []
    citire_automat(AFN)
