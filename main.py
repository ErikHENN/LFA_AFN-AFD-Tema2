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

'''
@list - reprezinta lista de transformat in string
@return - stringul provenit din concatenarea elementelor listei
'''
def listToString(list):
    string = ''.join(list)
    return string

'''
@lista1, lista2 - Listele de reunit
@return - lista provenita din reuniunea lor
'''
def reunesteListe(lista1, lista2):
    return list(set().union(lista1, lista2))

'''
@litera - Litera pentru care se creeaza lista
@nod - Nodul pentru care se creeaza lista
@return - Returnez lista de noduri la care se ajunge cu litera
'''
def listaNoduriPeLitera(litera, nod = Nod):
    lista = []
    indexNod = 0
    for c in nod.Muchie.litera:
        if c is litera:
            lista.append(nod.Muchie.legatura[indexNod])
        indexNod = indexNod + 1
    return lista

def stareTranzitie(nod, AFN):
    stare = 'intermediar'
    for c in nod:
        if AFN.lista_noduri[int(c)].stare == 'initial':
            stare = AFN.lista_noduri[int(c)].stare
        if AFN.lista_noduri[int(c)].stare == 'f':
            stare = AFN.lista_noduri[int(c)].stare
    return stare
'''
@AFN - Reprezinta AFN-ul pentru care creez automatul. 
Ii setez default value ca fiind un obiect al clasei automat deoarece vreau sa-l fortez sa foloseasca acest tip de date

Creez lista de noduri (retiune ca string) ale automatului. Pe baza acestei liste creez DataFrame-ul PANDAS
avand ca index de linie lista de noduri (0,1,2,01,012,etc.) si ca index de coloana cate o litera din alfabetul automatei. 
De asemenea pe coloane adaug si coloana '@' ce reprezinta faptul ca nodul a fost sau nu vizitat si procesat.

Dupa ce imi generez structura tabelului, completez prima parte cu nodurile simple ale AFN-ului, punand pe pozitia
(litera, nod) din tabel, reprezentat in format  (coloana, linie), lista de noduri in care se poate ajunge din nodul @nod
cu litera @litera.

Dupa ce am generat prima parte a tabelului, marchez toate noduri ca fiind nevizitate, adaugand FALSE pe coloana '@'

Mai departe generez nodurile combinate parcurgand progresiv, toate nodurile pentru fiecare litera, 
si creez linie noua pentru noua combinatie de tranzitii rezultata din reuniunea elementelor
functiei tranzitiei curente cu litera curenta.


In final parcurg din nou tabelul si il completez similar procedeului de mai sus atunci cand gasesc o valoare 'False' 
in dreptul unei litere. Este nevoie sa ma intorc deoarece, in timp ce generez tranzitii noi pentru litera 'b' spre exemplu
acestea vor apara si pentru litera 'a' (valoare in tabel fiind initializata prin False) la care nu ma 
voi intoarce prin generarea tuturor tranzitiilor noi din AFD.

'''
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
'''
@AFN - AFN-ul de transformat
@AFD - AFD-ul rezultat
Functia interpreteaza tabelul si il transpune, creand AFD-ul in formatul definit la citire
'''

def conversie(AFN = Automat, AFD = Automat):
    global lista_noduri
    table = creeazaTabelAutomat(AFN)
    print (table)
    print()
    AFD.nr_noduri = len(table.index)
    AFD.alfabet = AFN.alfabet
    ok = True
    for litera in list(AFN.alfabet):
        tranzitie = lista_noduri[0]
        tranzitie_legatura = listToString(table[litera][tranzitie])
        while tranzitie != tranzitie_legatura:
            print (tranzitie + " -> ( " + litera + " )" + tranzitie_legatura + " Stare = " + stareTranzitie(tranzitie, AFN))
            tranzitie = tranzitie_legatura
            tranzitie_legatura = listToString(table[litera][tranzitie])
        else:
            print(tranzitie + " -> ( " + litera + " )" + tranzitie_legatura  + " Stare = " + stareTranzitie(tranzitie, AFN))
            if lista_noduri.index(tranzitie) + 1 < len(lista_noduri):
                tranzitie = str(lista_noduri.index(tranzitie) + 1)
            tranzitie_legatura = listToString(table[litera][tranzitie])
        while lista_noduri.index(tranzitie) + 1 < len(lista_noduri):
            if tranzitie == tranzitie_legatura:
                print(tranzitie + " -> ( " + litera + " )" + tranzitie_legatura  + " Stare = " + stareTranzitie(tranzitie, AFN))
                tranzitie = lista_noduri[lista_noduri.index(tranzitie) + 1]
            tranzitie_legatura = listToString(table[litera][tranzitie])


'''
Afisez AFD-ul nou dupa urmatorul model:
- Eticheta nod
- Stare nod
- Numar de legaturi (muchii) ale nodului
- Legaturile automatului in format (nod_de_legatura, litera_acceptata_pe_legatura)
- Despart fiecare nod prin "------------" pentru claritate la citirea rezultatului
'''

'''
def conversie(AFN = Automat, AFD = Automat):
    table = creeazaTabelAutomat(AFN)
    for i in li
    
    nrn = AFD.nr_noduri
    for i in range(int(nrn)):
        print ("Eticheta nod: " + str(AFD.lista_noduri[i].eticheta))
        print("Stare nod: " + str(AFD.lista_noduri[i].stare))
        # nrm =  ("Nr. de legaturi ale nodului i"
        nrm = AFD.lista_noduri[i].nrm
        print ("Numar de muchii nod: " + str(nrm))
        for j in range(int(nrm)):
            # leg.append = "ID nod cu care se leaga nodul i"
            print("(" + AFD.lista_noduri[i].Muchie.legatura[j] + ", " + AFD.lista_noduri[i].Muchie.litera[j] + ")")
        print("------------")
        '''



def verifica_cv(AFD, cuvant):
    ok = 1
    nod = 0
    for c in cuvant:
        lista_ponderi = AFD.lista_noduri[nod].Muchie.litera
        lista_legaturi = AFD.lista_noduri[nod].Muchie.legatura
        if c in lista_ponderi:
            indexMuchie = lista_ponderi.index(c)
            nod = int(lista_legaturi[indexMuchie])
        else:
            ok = 0
            break
    if ok == 1 and AFD.lista_noduri[nod].stare is 'f':
        print ("Cuvant acceptat")
    elif ok == 0 and AFD.lista_noduri[nod].stare is 'f' and cuvant is '':
        print ("Cuvant acceptat")
    else:
        print ("Cuvant respins")
'''
# Functia main
# 1) Deschid fisierul afn.in
# 2) Apelez functia de citire automat
# 3) Convertesc AFN-ul in AFD
# 4) Apelez functia de afisare
'''


if __name__ == "__main__":
    optiune = input ("Alegeti optiunea [1 = Verifica cuvant AFD / 2 = Transformare AFN - AFD] : ")
    if int(optiune) == 1:
        file = open("afd.in", "r")
        cuvant = input ("Cuvantul de verificat este: ")
        AFD = Automat("abc")
        citire_automat(AFD)
        verifica_cv(AFD, cuvant)

    if int(optiune) == 2:
        file = open("afn.in", "r")
        AFN = Automat("ab")
        AFD = Automat("ab")
        citire_automat(AFN)
        conversie(AFN, AFD)