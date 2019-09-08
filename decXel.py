import pymysql
import xlsxwriter
from PyQt5.QtCore		import Qt 
from PyQt5 					import QtWidgets
#from datetime import date

class decXel:
	def __init__(self,  theWin, theConn):
		self.win		= theWin
		self.conn	= theConn
		
	def showDecompte( self ):
		theFName, selectedFilter = QtWidgets.QFileDialog.getSaveFileName(
			self.win,
			"Fichier a exporter",
			"",
			self.win.tr("*.xlsx"),
			None)
			
		conn 		= self.conn
		wk 		= xlsxwriter.Workbook('test.xlsx')
		wt 		= wk.add_worksheet()

		bold		= wk.add_format({'bold':True})
		num		= wk.add_format()
		num.set_num_format("###'###.00")
		dt			= wk.add_format({'align':'center'})
		dt.set_num_format("d mmmm yyyy")
		hrs		= wk.add_format()
		hrs.set_num_format("hh:mm")
		border1	= wk.add_format({'border':1})
		border1.set_border(1)
		border2	= wk.add_format({'border':4})
		border2.set_border(4)
		
		wt.set_column(0, 0, 30)
		wt.set_column(1, 1, 15)
		wt.set_column(2, 2, 5)
		wt.set_column(3, 3, 20)
		wt.set_column(4, 4, 6)

		wt.write_row('A1', ('Nom du badge', 'Litrage','', 'Date', 'Heure'))
		deb	= self.win.DDDebut.date().toString(Qt.ISODate)
		fin		= self.win.DDFin.date().toString(Qt.ISODate)
		sql = "SELECT DISTINCT  Carte,(SELECT nom FROM t_cards WHERE id LIKE Carte),FLOOR(MID(Carte,7,12)) FROM t_tankdaten "
		sql = sql + "WHERE BDate BETWEEN '"+deb+"' AND '"+fin+"' ORDER BY Carte"
		total	= 0
		try:
			cur 		= conn.cursor()
			cur. execute(sql)
			records 	= cur.fetchall()	
			line		= 1
			for row in records:
				line = line +1
				try:
					sql = "SELECT DISTINCT Calcul_total_card('"+row[0]+"','"+deb+"','"+fin+"') FROM t_tankdaten"
					c1 = conn.cursor()
					c1.execute(sql )
					rec1 = c1.fetchall()
					for r in rec1:
						wt.write_string('A%d'%line, row[1], bold)
						wt.write_number('B%d'%line, r[0], num)
						total += r[0]
						wt.write_string('C%d'%line, "Litres")
						wt.conditional_format(line, 0, line, 3,{'type':'no_error',   'format':border2} )
						wt.conditional_format(line, 0, line, 3,{'type':'error',   'format':border2} )

				except pymysql.Error as e:
					print( sql )
					print( e )				
				
				hl = line
				try: # DATE_FORMAT(BDate,'%d/%c/%Y'),DATE_FORMAT(BTime,'%k:%i')
					sql = "SELECT BDate,BTime, Litres FROM t_tankdaten WHERE Carte LIKE '"+row[0]+"' AND BDate BETWEEN '"+deb+"' AND '"+fin+"' "
					c1 = conn.cursor()
					c1.execute(sql )
					rec1 = c1.fetchall()
					for r in rec1:
						line = line +1
						wt.write_number('B%d'%line,  r[2],  num )
						wt.write_string('C%d'%line, "Litres" )
						wt.write_datetime('D%d'%line, r[0],  dt )
						wt.write_datetime('E%d'%line, r[1],  hrs)

				except pymysql.Error as e:
					print( sql )
					print( e )				
				wt.conditional_format(hl, 0, line, 5, {'type':'no_error', 'format':border1})
#				wt.write_formula('D%d'%hl, 'SUM(B%d:B%d'%(hl+1, line),num)
			cur.close()
			
		except pymysql.Error as e:
			print( e )
		line +=2
		wt.write_string('A%d'%line, "Total :", bold )		
		wt.write_number('B%d'%line, total,  num )
		wt.write_string('C%d'%line, "Litres" )
		
		wk.close()	
