import pymysql
from fpdf import FPDF
from PyQt5.QtCore		import Qt 
from PyQt5 					import QtWidgets


class decPdf:
	def __init__(self,  theWin, theConn):
		self.win 		= theWin
		self.conn	= theConn
		
	def showDecompte( self ):
		theFName, selectedFilter = QtWidgets.QFileDialog.getSaveFileName(
			self.win,
			"Fichier a exporter",
			"",
			self.win.tr("*.pdf"),
			None)
			
		conn 		= self.conn
		pdf = FPDF()
		pdf.add_page()
		pdf.set_font('Arial', 'B', 8)
		cell	= {'A':30, 
					'B':15, 
					'C':10, 
					'D':20, 
					'E':6}
		hc		= 4
		hmarg = 20

		pdf.set_x(hmarg)
		pdf.cell(cell['A'], hc,"Nom du badge" )
		pdf.cell(cell['B'], hc, 'Litrage' , 0, 0, 'R')
		pdf.cell(cell['C'], hc,"Litres" )
		pdf.cell(cell['D'], hc,'Date' )
		pdf.cell(cell['E'], hc,'Heure', 0, 1)
		#wt.write_row('A1', ('Nom du badge', 'Litrage','', 'Date', 'Heure'))
		deb	= self.win.DDDebut.date().toString(Qt.ISODate)
		fin		= self.win.DDFin.date().toString(Qt.ISODate)		
		sql = "SELECT DISTINCT  Carte,(SELECT nom FROM t_cards WHERE id LIKE Carte),FLOOR(MID(Carte,7,12)) FROM t_tankdaten "
		sql = sql + "WHERE BDate BETWEEN '"+deb+"' AND '"+fin+"' ORDER BY Carte"
		total	= 0
		try:
			cur 		= conn.cursor()
			cur. execute(sql)
			records 	= cur.fetchall()	
			for row in records:
				try:
					sql = "SELECT DISTINCT Calcul_total_card('"+row[0]+"','"+deb+"','"+fin+"') FROM t_tankdaten"
					c1 = conn.cursor()
					c1.execute(sql )
					rec1 = c1.fetchall()
					for r in rec1:
						pdf.set_font('Arial', 'B', 8)
						pdf.set_x(hmarg)
						pdf.cell(cell['A'], hc*2, row[1])
						pdf.cell(cell['B'], hc*2, '%9.2f'%r[0], 0, 0, 'R')
						total += r[0]
						pdf.cell(cell['C'], hc*2, "Litres", 0, 1)

				except pymysql.Error as e:
					print( sql )
					print( e )				
				

				try: # DATE_FORMAT(BDate,'%d/%c/%Y'),DATE_FORMAT(BTime,'%k:%i')
					sql = "SELECT  DATE_FORMAT(BDate,'%d/%c/%Y'),DATE_FORMAT(BTime,'%k:%i'), Litres FROM t_tankdaten WHERE Carte LIKE '"+row[0]+"' AND BDate BETWEEN '"+deb+"' AND '"+fin+"' "
					c1 = conn.cursor()
					c1.execute(sql )
					rec1 = c1.fetchall()
					for r in rec1:
						pdf.set_font('Arial', '', 8)
						pdf.set_x(hmarg+cell['A'])
						pdf.cell(cell['B'], hc, '%9.2f'%r[2] , 0, 0, 'R')
						pdf.cell(cell['C'], hc,"Litres" )
						pdf.cell(cell['D'], hc, r[0] )
						pdf.cell(cell['E'], hc, r[1], 0, 1)

				except pymysql.Error as e:
					print( sql )
					print( e )				
			cur.close()
			
		except pymysql.Error as e:
			print( e )
		try:
			pdf.set_x(hmarg)
			print("Doing the Total")
			pdf.set_font('Arial', 'B', 8)
			pdf.cell(cell['A'], hc*2, "Total :" )		
			pdf.cell(cell['B'],hc*2,  '%9.2f'%total, 0, 0, 'R')
			pdf.cell(cell['C'], hc*2, "Litres" , 0, 1)
			print(theFName)
			pdf.output(theFName, 'F')	
		except :
			None
