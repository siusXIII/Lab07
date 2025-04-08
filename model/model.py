import copy

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self._sequenza_ottima = []
        self._costo_minimo = -1

    @staticmethod
    def getUmidita(mese):
        return MeteoDao.getUmidita(mese)



    def calcola_sequenza(self, mese):
        self._costo_minimo = -1
        self._sequenza_ottima = []
        situazioni_meta_mese = MeteoDao.get_situazione_meta_mese(mese)
        self._ricorsione([], situazioni_meta_mese)
        return self._sequenza_ottima, self._costo_minimo

    def _ricorsione(self, parziale, situazioni):
        #caso terminale:
        if len(parziale) == 15:
            costo = self._calcola_costo_tot(parziale)
            if (self._costo_minimo == -1) or (costo < self._costo_minimo):
                self._costo_minimo = costo
                self._sequenza_ottima = copy.deepcopy(parziale)
        else:
            day = len(parziale)+1
            for situazione in situazioni[(day-1)*3:day*3]:
                #if situazione.data.day == day:
                if self._vincoli(parziale, situazione):
                    parziale.append(situazione)
                    self._ricorsione(parziale, situazioni)
                    parziale.pop()

    def _vincoli(self, parziale, situazione) -> bool:
        counter = 0
        for fermata in parziale:
            if fermata.localita == situazione.localita:
                counter += 1
        if counter >= 6:
            return False

        if 2 >= len(parziale) > 0:
            if situazione.localita != parziale[0].localita:
                return False

        elif len(parziale) > 2:
            sequenza_finale = parziale[-3:] # <- ultimi 3 giorni in parziale
            prima_fermata = sequenza_finale[0].localita # < primo di questi ultimi tre giorni
            counter = 0
            for fermata in sequenza_finale:
                if fermata.localita == prima_fermata:
                    counter += 1
            if (counter < 3) and situazione.localita != sequenza_finale[-1].localita:
                return False
        return True

    def _calcola_costo_tot(self, parziale):
        costo = 0
        for i in range(len(parziale)):
            costo += parziale[i].umidita
        return costo