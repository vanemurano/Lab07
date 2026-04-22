from database.meteo_dao import MeteoDao as md


class Model:
    def __init__(self):
        pass

    def getMediaUmidita(self, mese):
        return md.getMediaUmidita(mese)