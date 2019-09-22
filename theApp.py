from PyQt5 					import QtWidgets
from PyQt5.QtCore		import Qt 
from PyQt5.QtWidgets 	import QApplication,  QTableWidgetItem, QTreeWidgetItem#, QMessageBox
from PyQt5.QtGui			import QFont

import pymysql
#from settings 					import settings
#from t_cards 					import t_cards
#from decXel 					import decXel
#from decPdf					import decPdf
#from datetime 				import date

class theApp( QApplication ):
	
####################################################################################################
#	ssetConnection																												#
#																																	#
####################################################################################################

	def setConnection(self,  theConn):
		self.conn	= theConn
		
####################################################################################################
#	setCard																														#
#																																	#
####################################################################################################

	def setCard(self,  theCards):
		self.cards	= theCards
		
####################################################################################################
#	import_file																													#
#																																	#
####################################################################################################

	def import_file( self, win,  Gest ):
		theFName, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(
			win,
			"",
			"",
			win.tr("*.rtx"),
			None)

		WA			= str( Gest.thePref.elems[ 0 ]['WANumber'] )
		loop			= 4
		WANum		= 0
		STNum		= 0
		RECType		= 0

		Totaux		= {}

		theFile		= open( theFName,  "r")
		cur 			= self.conn.cursor()
		
		while( (loop ) ):
			theLine	= theFile.readline()
			RECType	= theLine[0:2]
			WANum	= theLine[2:8]
			STNum	= theLine[8:12]
			
			if(RECType == "26"):
				Year		= "20"+theLine[12:14]
				Mounth	= theLine[14:16]
				Day		= theLine[16:18]
				Hours		= theLine[18:20]
				Minutes	= theLine[20:22]
				
				print("Start", WANum, STNum, Day, Mounth,  Year,  Hours,  Minutes)
			elif(RECType == "27"):
				RArt		=  theLine[12:14]
				TNum		=  theLine[14:18]
				Year		= "20"+theLine[18:20]
				Mounth	= theLine[20:22]
				Day		= theLine[22:24]
				Hours		= theLine[24:26]
				Minutes	= theLine[26:28]
				BArt		= theLine[28:30]
				CNum		= theLine[30:50]
				IDNum	= theLine[50:56]
				GeBet	= theLine[56:62]
				TermID	= theLine[62:66]
				KM		= theLine[68:74]
				Noten	= theLine[74:80]
				Saule		= theLine[80:82]
				Carbu	= theLine[82:84]
				Prix		= theLine[84:90]
				Litres		= int( theLine[90:96] ) / 100
				Montant	= int( theLine[96:102] ) / 100
				CodeFin	= theLine[102:104]
				
				if WANum == WA:
					param = (
						theLine, 
						WANum, 
						STNum, 
						RArt, 
						TNum, 
						Year+"/" +
						Mounth+"/"+
						Day, 
						Hours+":"+
						Minutes, 
						BArt, 
						CNum, 
						IDNum, 
						GeBet, 
						TermID, 
						KM, 
						Noten, 
						Saule, 
						Carbu, 
						Prix, 
						str(Litres)	, 
						str(Montant), 
						CodeFin, 
						)
						
					try:
						sql = """INSERT INTO t_tankdaten VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
						cur.execute(sql,  param)
						self.conn.commit()
					except :
						self.conn.rollback()
					try:
						sql = """INSERT INTO t_cards VALUE(%s,%s,%s,%s,%s,%s)"""
						cur.execute(sql,  (CNum, '', '', '', '', 'Non definie'))
						self.conn.commit()
					except :
						self.conn.rollback()
						
					if( CNum in Totaux):
						Totaux[CNum] ["total"]+= Litres
						Totaux[CNum] [Day+ "/" + Mounth+ "/" +Year+" "+  
							Hours+":"+Minutes]= Litres

					else:
						Totaux[CNum] = {}
						Totaux[CNum] ["total"]= Litres
						Totaux[CNum] [Day+ "/" + Mounth+ "/" +Year+" "+  
							Hours+":"+Minutes]= Litres
						
				else:
					print( "BAD Automate Number MUST %8s was %8s"%(WA, WANum ) )
				#loop -= 1
			elif(RECType == "29"):
				print( "End")
				loop = 0

		theFile.close()
		cur.close()
		self.showTransaction( win )
		self.showDecompte( win )
		self.cards.loadCards()

#####################################################################################################
#	showTransaction																																													#
#																																																		#
#####################################################################################################

	def showTransaction(self,  win):
		win.v_transactions.clear(  )
		win.v_transactions.setColumnCount(4)
		win.v_transactions.setHorizontalHeaderLabels(("Date", "Heure", "Badge", "Litres"))
		deb	= win.DTDebut.date().toString(Qt.ISODate)
		fin		= win.DTFin.date().toString(Qt.ISODate)
		sql 	= "SELECT DATE_FORMAT(BDate,'%d/%c/%Y'),DATE_FORMAT(BTime,'%k:%i'),decode_memopass(Carte,WA),Litres FROM t_tankdaten "
		sql 	= sql + "WHERE BDate BETWEEN '"+deb+"' AND '"+fin+"' ORDER BY BDate,BTime"
		total 	= 0
		try:
			cur = self.conn.cursor()
			cur. execute(sql)
			records = cur.fetchall()
			win.v_transactions.setRowCount( len( records ))
			q = 0
			
			for row in records:
				win.v_transactions.setItem(q, 0,QTableWidgetItem( row[0] ))
				win.v_transactions.setItem(q, 1,QTableWidgetItem( row[1] ))
				win.v_transactions.setItem(q, 2,QTableWidgetItem( str( row[2] )) )
				win.v_transactions.setItem(q, 3,QTableWidgetItem( str( row[3] )) )
				total	+=	row[ 3 ]
				q +=1
			cur.close()
		except pymysql.Error as e:
			print( e )
			
#####################################################################################################
#	showDecompte																																													#
#																																																		#
#####################################################################################################
		
	def showDecompte(self,  win):
		win.t_decompte.clear( )
		win.t_decompte.setColumnCount( 1 )

		deb	= win.DDDebut.date().toString(Qt.ISODate)
		fin		= win.DDFin.date().toString(Qt.ISODate)
		
		sql = "SELECT DISTINCT  Carte,CONCAT((SELECT nom FROM t_cards WHERE id LIKE Carte),' (',FLOOR(MID(Carte,7,12)),')') FROM t_tankdaten "
		sql = sql + "WHERE BDate BETWEEN '"+deb+"' AND '"+fin+"' ORDER BY Carte,M27"
		
		total 	= 0
		font	= QFont( 'Courier', 10)
		font1	= QFont( 'Courier', 12)
		font1.setBold( True )
		try:
			cur = self.conn.cursor()
			cur. execute(sql)
			records = cur.fetchall()	
			
			for row in records:
				item = QTreeWidgetItem( win.t_decompte )
				item.setFont( 0, font )
				try:
					sql = "SELECT Calcul_total_card('"+row[0]+"','"+deb+"','"+fin+"') FROM t_tankdaten"
					c1 = self.conn.cursor()
					c1.execute(sql )
					rec1 = c1.fetchall()
					for r in rec1:
						try:
							if row[1]:
								item.setText( 0, "%-40s -> %8.2f Litres" %(  row[1],  r[0] ))
							else:
								item.setText( 0, "Carte inconnue [%s] -> %8.2f Litres" % (row[ 0 ], r[ 0 ]))
						except:
							None

				except pymysql.Error as e:
					print( sql )
					print( e )				
					
				try:
					sql = "SELECT DATE_FORMAT(BDate,'%d/%c/%Y'),DATE_FORMAT(BTime,'%k:%i'), Litres FROM t_tankdaten WHERE Carte LIKE '"+row[0]+"' AND BDate BETWEEN '"+deb+"' AND '"+fin+"' ORDER BY M27"
					c1 = self.conn.cursor()
					c1.execute(sql )
					rec1 = c1.fetchall()
					for r in rec1:
						i 		= QTreeWidgetItem( item )
						i.setText( 0, r[0]+" "+ r[1] +"-> %8.2f Litres" % r[2] )
						total	+= r[ 2 ]
						item.addChild( i )

				except pymysql.Error as e:
					print( sql )
					print( e )				
					
				win.t_decompte.addTopLevelItem( item )
			cur.close()
		except pymysql.Error as e:
			print(sql)
			print( e )
		
		header	=  win.t_decompte.headerItem()
		header.setFont( 0,  font1 )
		header.setText( 0,"Consomation totale du décompte: %8.2f Litres"%total  ) 	
