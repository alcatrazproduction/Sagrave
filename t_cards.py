from PyQt5				import QtWidgets,QtCore, uic
from PyQt5.QtWidgets 	import QApplication,  QTableWidgetItem, QTreeWidgetItem
import pymysql



class t_cards:
	tbName	=	't_cards'
#	id 			VARCHAR(20)
#	nom		VARCHAR(45)
#-	vehicule	VARCHAR(45)
#	no_plaque	VARCHAR(45)
#	code		VARCHAR(10)
#	remarque	TEXT

	def __init__(self,  theWin, theConn, theApp):
		self.win 		= theWin
		self.conn	= theConn
		self.app		= theApp
		
	def loadCards(self):
		sql	= 'SELECT floor (mid(id,7,12)),nom,vehicule,no_plaque,remarque,id FROM '+self.tbName+' ORDER BY id'
		win = self.win
		win.v_cards.setColumnCount(5)
		win.v_cards.setHorizontalHeaderLabels(("Numero", "Nom", "Véhicule", "Numéro Plaque", "Remarque"))
		try:
			cur = self.conn.cursor()
			cur. execute(sql)
			records = cur.fetchall()
			win.v_cards.setRowCount( len( records ))
			q = 0
			
			for row in records:
				id	= QTableWidgetItem( "%5.0f"%row[0] )
				id.setData(0x0100,  row[5])
				win.v_cards.setItem(q, 0, id)
				win.v_cards.setItem(q, 1,QTableWidgetItem( row[1] ))
				win.v_cards.setItem(q, 2,QTableWidgetItem( str( row[2] )) )
				win.v_cards.setItem(q, 3,QTableWidgetItem( str( row[3] )) )
				win.v_cards.setItem(q, 4,QTableWidgetItem( str( row[4] )) )
				q +=1
			cur.close()
		except pymysql.Error as e:
			print( e )

	def editCards(self):
		win 		= self.win
		v_cards	=win.v_cards
		theRow	= v_cards.selectedItems()
		sql	= 'SELECT floor (mid(id,7,12)),nom,vehicule,no_plaque,code,remarque,id FROM '+self.tbName+' WHERE id LIKE "'+theRow[0].data(0x0100)+'"'
		dlg 	= uic.loadUi("modal_card.ui")
		pt 	= dlg.form
		card = -1
		try:
			cur = self.conn.cursor()
			cur. execute(sql)
			records = cur.fetchall()
			for row in records:
				pt.itemAt(1).widget().setText("%5.0f"%row[0])
				pt.itemAt(3).widget().setText(row[1])
				pt.itemAt(5).widget().setText(row[2])
				pt.itemAt(7).widget().setText(row[3])
				pt.itemAt(9).widget().setText(row[4])
				pt.itemAt(11).widget().setText(row[5])
				card	= row[6]
			cur.close()
		except pymysql.Error as e:
			print( e )
		ret 	= dlg.exec()
		if ret == 1:
			nom			= pt.itemAt(3).widget().text()
			vehicule		= pt.itemAt(5).widget().text()
			imma			= pt.itemAt(7).widget().text()
			secret		=	pt.itemAt(9).widget().text()
			remarque	=pt.itemAt(11).widget().text()
			theRow[1].setText( nom )
			theRow[2].setText( vehicule )
			theRow[3].setText( imma )
			theRow[4].setText( remarque )
			try:
				cur 	= self.conn.cursor()
				sql	= "UPDATE %s SET nom='%s', vehicule='%s', no_plaque='%s', code='%s', remarque='%s' WHERE id LIKE '%s'"%(
					self.tbName, nom, vehicule, imma, secret, remarque, card)
				cur. execute(sql)
				cur.close()
				self.conn.commit()
			except pymysql.Error as e:
				print( e )
		
			
	
