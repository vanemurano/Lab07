import copy
from datetime import date
from time import time

from database.meteo_dao import MeteoDao as md


class Model:
    def __init__(self):
        self.lista_loc=self.getAllLocalita()
        self._situazioni=self.get_all_situazioni()

    def getMediaUmidita(self, mese):
        return md.getMediaUmidita(mese)

    def get_all_situazioni(self):
        return md.get_all_situazioni() # ritorna la lista di tutte le situazioni
     # ordinate per data crescente

    def get_situazioni_data(self, data: date) -> dict:
        res={}
        for sit in self._situazioni:
            if sit.data==data:
                res[sit.localita]=sit
        return res
    # ritorna un dizionario di situazioni per quella data
    # dove la chiave è la località

    def getAllLocalita(self):
        return md.getAllLocalita()

    def calcola(self, mese: int):
        self.best_costo=2500 # costo irraggiungibile, solo per iniziare il confronto
        self.best_soluzione=[]
        data = date(2013, mese, 1) # crea un oggetto di tipo date
        self._ricorsione([], data, 0)
        # inizio ricorsione, parziale vuoto e giorno 1 del mese
        return self.best_soluzione, self.best_costo

    def _ricorsione(self, parziale, data: date, totale):  # parziale è una lista di situazioni
        # passa alla prossima se già il totale è più alto del costo migliore finora
        if totale>=self.best_costo:
            return
        # condizione terminale:
        if len(parziale)==15: # ho riempito i 15 giorni
            if totale<self.best_costo:
                self.best_costo=totale
                self.best_soluzione=copy.deepcopy(parziale)
                # memorizzo costo e soluzione migliori come attributi dell'oggetto
            return
        # non ritorno nulla perché ho già fatto il confronto e salvato i risultati
        # condizione ricorsiva:
        else:
            for loc in self.lista_loc:
                if self.conta_localita(parziale, loc)>=6:
                    # se il tecnico ha già trascorso i max 6 giorni in quella città
                    continue
                if self.cambio_citta(parziale, loc):
                    # fa il controllo solo se voglio cambiare città
                    if not self.controllo_giorni_consecutivi(parziale):
                        continue # passa alla prossima città
                sit=self.get_situazioni_data(data)[loc]
                nuovo_costo=sit.umidita
                # calcolo quanto costerebbe passare alla città loc
                if self.cambio_citta(parziale, loc):
                    nuovo_costo += 100
                parziale.append(sit)
                self._ricorsione(parziale, self.aumento_data(data, 1), totale+nuovo_costo)
                parziale.pop() #BACKTRACKING: provo le altre città

    def cambio_citta(self, sequenza, citta) -> bool:
        if len(sequenza)>0:
            ultima = sequenza[-1].localita
            if ultima!=citta:
                return True
        return False

    def controllo_giorni_consecutivi(self, sequenza) -> bool:
        # controllo se sono stato nell'ultima città per almeno 3 giorni di fila
        if len(sequenza)<3:
            return False
        ultima_citta=sequenza[-1].localita
        if sequenza[-2].localita==sequenza[-3].localita==ultima_citta:
            return True
        return False

    def aumento_data(self, data: date, num: int):
        giorno=data.day # estraggo il giorno
        mese=data.month
        return date(2013, mese, giorno+num)

    def conta_localita(self, lista_sit, citta):
        # analizza la lista di situazioni per vedere quante volte compare quella città
        conta=0
        for sit in lista_sit:
            if sit.localita==citta:
                conta+=1
        return conta