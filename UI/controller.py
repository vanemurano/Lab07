import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.clean() # ripulisce la listview
        mese=self._view.dd_mese.value
        if mese is None:
            self._view.create_alert("Selezionare un mese!")
            return
        self._view.lst_result.controls.append(
            ft.Text("L'umidità media nel mese selezionato è"))
        for row in self._model.getMediaUmidita(mese):
            self._view.lst_result.controls.append(
                ft.Text(f"{row[0]}: {row[1]}"))
        self._view.update_page()

    def handle_sequenza(self, e):
        self._view.lst_result.clean()  # ripulisce la listview
        if self._view.dd_mese.value is None:
            self._view.create_alert("Selezionare un mese!")
            return
        mese = int(self._view.dd_mese.value)
        self._view.lst_result.controls.append(
            ft.Text(f"La soluzione ottima ha costo {self._model.calcola(mese)[1]} ed è:"))
        for situazione in self._model.calcola(mese)[0]:
            self._view.lst_result.controls.append(
                ft.Text(situazione))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value) # passa il numero selezionato come valore

