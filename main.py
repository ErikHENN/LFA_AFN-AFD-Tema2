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


def listToString(list):
    string = ''.join(list)
    return string
def listeazaStariFinale(AFN = Automat):
    lista_stari_finale = []
    for i in AFN.lista_noduri:
        if AFN.lista_noduri[i].stare is 'f':
            lista_stari_finale.append(i)
    return lista_stari_finale

def reunesteListe(lista1, lista2):
    return list(set().union(lista1, lista2))


def listaNoduriPeLitera(litera, nod = Nod):
    lista = []
    indexNod = 0
    for c in nod.Muchie.litera:
        if c is litera:
            lista.append(nod.Muchie.legatura[indexNod])
        indexNod = indexNod + 1
    return lista


def creeazaTabelAutomat(AFN = Automat):
    global lista_noduri
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
            if table['@'][nod] is False or table[litera][nod] is False:
                if lista_de_tranzitii is not False:
                    if len(lista_de_tranzitii) > 1:
                        eticheta_tranzitie_noua = ''.join(lista_de_tranzitii)
                    else:
                        eticheta_tranzitie_noua = lista_de_tranzitii[0]
                else:
                    eticheta_tranzitie_noua = nod
                for c in eticheta_tranzitie_noua:
                    tranzitie_noua = reunesteListe(tranzitie_noua, table[litera][c])
                    table['@'][c] = True
                if eticheta_tranzitie_noua not in lista_noduri:
                    lista_noduri.append(eticheta_tranzitie_noua)
                if eticheta_tranzitie_noua not in table.index:
                    table.loc[eticheta_tranzitie_noua] = False
                table.loc[eticheta_tranzitie_noua][litera] = tranzitie_noua
                table['@'][nod] = True
    #Verific si completez golurile tabelului in caz ca exista
    for litera in list(AFN.alfabet):
        for nod in lista_noduri:
            tranzitie_noua = []
            if table[litera][nod] is False:
                for c in nod:
                    tranzitie_noua = reunesteListe(tranzitie_noua, table[litera][c])
                table.loc[nod][litera] = tranzitie_noua

    return table

def conversie(AFN = Automat, AFD = Automat):
    global lista_noduri
    table = creeazaTabelAutomat(AFN)
    AFD.nr_noduri = len(table.index)
    AFD.alfabet = AFN.alfabet

    for i in table.index:
        legatura = []
        litera_acceptata = []
        eticheta = i
        print("ET = " + eticheta)
        nr_muchii = 0

        #Pentru nodul i calculez lungimea fiecarei liste de pe coloanele literelor
        for litera in list(AFD.alfabet):
            nr_muchii = nr_muchii + len(table[litera][i])
            for j in table[litera][i]:
                if AFN.lista_noduri[int(j)].stare is 'f':
                    stare = 'f'
                elif AFN.lista_noduri[int(j)].stare == 'initiala':
                    stare = 'initiala'
                else:
                    stare = 'intermediara'

        for j in range(int(nr_muchii)):
            for litera in list(AFD.alfabet):
                legatura.append(listToString(table[litera][i]))
                litera_acceptata.append(litera)
        M = Muchie(legatura, litera_acceptata)
        N = Nod(eticheta, stare, nr_muchii, M)
        AFD.adauga_nod(N)
    print (table)

def afisare(AFD = Automat):
    nrn = AFD.nr_noduri
    for i in range(int(nrn)):
        print ("Eticheta nod: " + str(AFD.lista_noduri[i].eticheta))
        print("Stare nod: " + str(AFD.lista_noduri[i].stare))
        # nrm =  ("Nr. de legaturi ale nodului i"
        nrm = AFD.lista_noduri[i].nrm
        print ("Numar de muchii nod: " + str(nrm))
        for j in range(int(nrm)):
            # leg.append = "ID nod cu care se leaga nodul i"
            print(AFD.lista_noduri[i].Muchie.legatura[j])
            # lit.append="Litera acceptata pe legatura [i, leg[j]]"
            print(AFD.lista_noduri[i].Muchie.litera[j])

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
    AFD = Automat("ab")
    citire_automat(AFN)
    conversie(AFN, AFD)
    afisare(AFD)