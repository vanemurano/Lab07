from datetime import datetime

from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result # ritorna una lista di tutte le situazioni

    @staticmethod
    def getAllLocalita() -> list:
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT distinct s.Localita
                                FROM situazione s"""
            cursor.execute(query)
            for row in cursor:
                result.append(row["Localita"])
            cursor.close()
            cnx.close()
        return result #ritorna una lista di località
    # utile se cambiamo database

    @staticmethod
    def getMediaUmidita(mese: int) -> list:
        cnx=DBConnect.get_connection()
        cursor=cnx.cursor(dictionary=True)

        query="""select localita, avg(umidita) as media_umidita
                from situazione 
                where month(data)=coalesce(%s, month(data))
                group by localita"""

        cursor.execute(query, (mese,))

        res=[]

        for row in cursor:
            res.append((row["localita"], row["media_umidita"])) # tupla: località, media

        cursor.close()
        cnx.close()

        return res # ritorna una lista di tuple
