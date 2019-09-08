#!/usr/bin/env python3
from PyQt5 					import	uic
from PyQt5.QtGui			import	QImage ,  QPixmap
from PyQt5.QtWidgets 	import 	QMessageBox

import pymysql
from datetime 				import	date
from time						import	sleep

from theApp					import	theApp
from settings 					import	settings
from t_cards 					import	t_cards
from dispatcher 				import dispatcher
		
class gestion:
	def __init__(self):
		self.app 			=	theApp([])
		self.thePref 	= settings( self.app )
		self.about		= uic.loadUi("about.ui")
		filename 		= r'logo.png'
		logo 				= QImage(filename )
		self.about.logo.setPixmap(QPixmap.fromImage(logo))
		self.about.info.setText("Initialising Application")
		self.about.show()
		sleep(2)
		
	def	initDatabase(self):
		self.about.info.setText("Trying to connect to database")
		thePref			= self.thePref
		
		while 1:
			try:
				#conn = pymysql.connect(host='localhost', port=3306, user='sagrave', passwd='', db='sagrave_ouchy')
				conn = pymysql.connect(	host		= thePref.elems['DBHost'], 
													port		= int( thePref.elems['DBPort'] ), 
													user		= thePref.elems['DBUser'], 
													passwd	= thePref.elems['DBPass'], 
													db			= thePref.elems['DBdb'])

				cur = conn.cursor()
				break
			except pymysql.Error as e:
				if e.args[0] == 1049:
					print('Unknow Database')
					msgBox	= QMessageBox() 
					msgBox.setText("La base de donnée existe pas")
					msgBox.setInformativeText("Voulez-vous la créer")
					msgBox.setStandardButtons(QMessageBox.Ok  | QMessageBox.Cancel)
					msgBox.setDefaultButton(QMessageBox.Cancel)
					ret = msgBox.exec()
					if ret == QMessageBox.Ok:
						try:
							conn = pymysql.connect(	host		= thePref.elems['DBHost'], 
																port		= int( thePref.elems['DBPort'] ), 
																user		= thePref.elems['DBUser'], 
																passwd	= thePref.elems['DBPass'], 
																)
							cur = conn.cursor()
							cur.execute("CREATE DATABASE IF NOT EXISTS '%s'"% ( thePref.elems['DBdb'] ))
							cur.close()
							conn.close()
						except pymysql.Error as e1:
							print(e1)
							print("CREATE DATABASE IF NOT EXISTS %s"% ( thePref.elems['DBdb']+'test' ))
							  
					else :
						  exit( -2 )
				print( e )
				ret =	thePref.showDialog()
				if ret == 0:
					exit(-1)

		self.app.setConnection( conn )
			
		try:
			cur.execute('SELECT COUNT(*) FROM t_tankdaten')
		except pymysql.Error as e:
			if e.args[0] == 1146:
				print('Tables do not exist')
				msgBox	= QMessageBox() 
				msgBox.setText("les tables ne sont pas présente")
				msgBox.setInformativeText("Voulez-vous les créer")
				msgBox.setStandardButtons(QMessageBox.Ok  | QMessageBox.Cancel)
				msgBox.setDefaultButton(QMessageBox.Cancel)
				ret = msgBox.exec()
				if ret == QMessageBox.Ok:
					sql	= ''
					try:
						f = open('schemas.sql', 'r')
						for l in f :
							sql 	= sql + ' ' + l
							if l.find(';') >=0:
								cur.execute(l)
								sql	= ''
					except pymysql.Error as e1:
						print(e1)
						print( sql )
					f.close()
				else :
					  exit( -3 )
			else:
				print(e)
				print(e.args[0])
				exit( -20 )
		self.conn	= conn

	def	 initApplication(self):
		win 		= uic.loadUi("sagrave.ui")
		dispatch	= dispatcher( win, self.app, self.conn)
		dispatch.setAbout( self.about )
		
		win.actionOuvrir.triggered.connect( lambda checked:  self.app.import_file( win ))
		win.actionQuitter.triggered.connect( win.close)
		win.actionApropos.triggered.connect( dispatch.doAbout )
		win.DExcel.clicked.connect(dispatch.createExcel)
		win.DPdf.clicked.connect(dispatch.createPdf)
		win.v_cards.doubleClicked.connect(dispatch.editKey)

		now 	= (date. today()).replace(day=1)
		mn 	= now.month+1
		if mn > 12:
			fin=now.replace(year=now.year+1, month=1)
		else:
			fin=now.replace( month=mn)
			

		win.DTDebut.setMaximumDate(fin)
		win.DTFin.setMaximumDate(fin)
		win.DDDebut.setMaximumDate(fin)
		win.DDFin.setMaximumDate(fin)

		mn 	= now.month-1
		if mn < 0:
			fin=now.replace(year=now.year-1, month=12)
		else:
			fin=now.replace( month=mn)
			
		win.DTDebut.setDate(fin)
		win.DTFin.setDate(now)
		win.DDDebut.setDate(fin)
		win.DDFin.setDate(now)

		win.DTDebut.dateChanged.connect(dispatch.dateTransaction)
		win.DTFin.dateChanged.connect(dispatch.dateTransaction)
		win.DDDebut.dateChanged.connect(dispatch.dateDecompte)
		win.DDFin.dateChanged.connect(dispatch.dateDecompte)

		self.about.info.setText("Loading Cards information...")

		self.cards	=	t_cards(win, self.conn, self.app)
		dispatch.setCards( self.cards )
		self.cards.loadCards()
		self.app.setCard( self.cards )
		self.about.info.setText("Creating Transactions...")

		self.app.showTransaction(win)
		self.about.info.setText("Creating Report...")
		sleep(2)
		self.app.showDecompte(win)
		self.win			= win
		self.dispatch	= dispatch
		
	def	mainLoop(self):
		self.about.close()
		self.about.info.setText("")
		self.win.show()
		ret = self.app.exec()
		#SELECT decode_memopass( Carte,WA) AS card,Litres, calcul_total_card( Carte,'2019/07/01','2019/08/01') FROM sagrave_ouchy.t_tankdaten GROUP BY Carte  ORDER BY Carte;

		self.conn.close()
		exit( ret )