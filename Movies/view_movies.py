#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PySide import QtGui, QtCore
from movies import Ui_MainWindow
import controlador

class Movies(QtGui.QMainWindow):
	columnas_tabla = (
			(u"Títutlo",200),
			(u"Año",100),
			(u"Director",150),
			(u"País", 100),
			(U"Ranking", 75)
			)

	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.load_movies()
		self.ui.btn_up.clicked.connect(self.action_btn_subir)
		self.ui.btn_down.clicked.connect(self.action_btn_bajar)
		self.messageDialog = QtGui.QMessageBox(self)
		self.show()

                
	def load_movies(self):
		movies =controlador.obtenerPeliculas()
		rows = len(movies)


		model = QtGui.QStandardItemModel(rows, len(self.columnas_tabla))
		self.ui.table_movies.setModel(model)
		self.ui.table_movies.horizontalHeader().setResizeMode(0,self.ui.table_movies.horizontalHeader().Stretch)

		for col, h in enumerate(self.columnas_tabla):
				model.setHeaderData(col, QtCore.Qt.Horizontal, h[0])
				self.ui.table_movies.setColumnWidth(col, h[1])

		for i, data in enumerate(movies):
				row = [data[1], data[3], data[4], data[5], data[8]]

				for j, field in enumerate(row):
						index=model.index(i,j,QtCore.QModelIndex())
						model.setData(index, field)
				model.item(i).mov = movies
		modelSel = self.ui.table_movies.selectionModel()
		modelSel.currentChanged.connect(self.tabla_cell_selected)

	def tabla_cell_selected(self,index):
		self.ui.widget_2.setVisible(True)

		model = self.ui.table_movies.model()
		rank = model.index(index.row(), 4, QtCore.QModelIndex()).data()
		movie = controlador.obtenerRank(rank)
		pmap = QtGui.QPixmap(str(movie[0]['poster']))

		self.ui.lbl_imagen.setPixmap(pmap)
		self.ui.lbl_reparto.setText(str(movie[0]['stars']))
		self.ui.lbl_descripcion.setText(str(movie[0]['description']))


	def action_btn_subir(self):
		model = self.ui.table_movies.model()
		index = self.ui.table_movies.currentIndex()
		if index.row()==-1:
			self.messageDialog.setText(u"Selecciones una pelicula")
			self.messageDialog.exec_()
		else:
			rank = model.index(index.row(), 4, QtCore.QModelIndex()).data()
			movie = controlador.obtenerRank(rank)
			rank_viejo= int(movie[0]['ranking'])
			rank_nuevo=rank_viejo-1
			if(rank_nuevo ==0):
				self.messageDialog.setText(u"No se puede subir más el rank.")
				self.messageDialog.exec_()
			else:
				movie_c=controlador.obtenerRank(rank_nuevo)
				controlador.actualizarDato(movie[0]['title'],rank_nuevo)
				if(movie_c):
					controlador.actualizarDato(movie_c[0]['title'],rank_viejo)
				self.load_movies()

	def action_btn_bajar(self):
		model = self.ui.table_movies.model()
		index = self.ui.table_movies.currentIndex()
		if index.row()==-1:
			self.self.messageDialog.setText(u"Seleccione una pelicula")
			self.messageDialog.exec_()
		else:
			rank = model.index(index.row(), 4, QtCore.QModelIndex()).data()
			movie = controlador.obtenerRank(rank)
			rank_viejo= int(movie[0]['ranking'])
			rank_nuevo=rank_viejo+1
			movie_c=controlador.obtenerRank(rank_nuevo)
			controlador.actualizarDato(movie[0]['title'],rank_nuevo)
			if(movie_c):
			    controlador.actualizarDato(movie_c[0]['title'],rank_viejo)
			self.load_movies()      




if __name__ == '__main__':
	app=QtGui.QApplication(sys.argv)
	main = Movies()
	sys.exit(app.exec_())
	
