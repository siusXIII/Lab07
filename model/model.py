from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        pass

    @staticmethod
    def getUmidita(mese):
        return MeteoDao.getUmidita(mese)
