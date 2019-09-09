#!/usr/bin/env python3
#######################################################################################################
#	Main class ( gestion) for the app																						#
#	Was the first writing in no class, don the main loop and init all the stuff								#
#	Creator:		Yves Huguenin																									#
#	Date:			06.09.2019																										#
#	Version:		0.1																												#
#																																		#
#######################################################################################################
from PyQt5 					import	uic
from PyQt5.QtGui			import	QImage ,  QPixmap
from PyQt5.QtWidgets 	import 	QMessageBox

import pymysql
from datetime 				import	date
from time					import	sleep

from theApp					import	theApp
from settings 				import	settings
from t_cards 				import	t_cards
from dispatcher 			import dispatcher
from constant			import const		
class gestion:
	def __init__(self):
		
		self.app 			= theApp([])
		self.thePref 	= settings( self.app )
		self.about		= uic.loadUi( const.aboutWindow)
		logo 				= QImage( const.logoFile )
		self.about.logo.setPixmap(QPixmap.fromImage(logo))
		self.about.info.setText("Initialising Application")
		self.about.show()
		sleep(2)
		
	def initDatabase(self):
		
		self.about.info.close()
		self.about.info.setText("Trying to connect to database")
		self.about.show()
		thePref			= self.thePref
		
		while 1:
			try:
				conn = pymysql.connect(	host		= thePref.elems[0]['DBHost'], 
													port		= int( thePref.elems[0]['DBPort'] ), 
													user		= thePref.elems[0]['DBUser'], 
													passwd	= thePref.elems[0]['DBPass'], 
													db			= thePref.elems[0]['DBdb'])

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
							conn = pymysql.connect(	host		= thePref.elems[0]['DBHost'], 
																port		= int( thePref.elems[0]['DBPort'] ), 
																user		= thePref.elems[0]['DBUser'], 
																passwd	= thePref.elems[0]['DBPass'], 
																)
							cur = conn.cursor()
							cur.execute("CREATE DATABASE IF NOT EXISTS '%s'"% ( thePref.elems[0]['DBdb'] ))
							cur.close()
							conn.close()
						except pymysql.Error as e1:
							print(e1)
							print("CREATE DATABASE IF NOT EXISTS %s"% ( thePref.elems[0]['DBdb'] ))
							  
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
						f = open( const.schemaFile , 'r')
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
		self.app.conn	= conn

	def initApplication(self):
		
		global primaryScreen
		
		win 				= uic.loadUi( const.mainWindow )
		dispatch			= dispatcher( win, self )
		primaryScreen	= self.app.primaryScreen()
		scrSize			= primaryScreen.size()
		win.move( scrSize.width()/2 - win.width()/2, scrSize.height()/2 - win.width()/2 )
		dispatch.resizeWindow()
		dispatch.setAbout( self.about )
		

		win.actionOuvrir.triggered.connect( lambda checked:  self.app.import_file( win, self ))
		win.actionQuitter.triggered.connect( win.close)
		win.actionApropos.triggered.connect( dispatch.doAbout )
		win.actionSetting.triggered.connect( dispatch.doPreferences )
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

		self.cards	=	t_cards(win, self.app)
		dispatch.setCards( self.cards )
		self.cards.loadCards()
		self.app.setCard( self.cards )
		self.about.info.setText("Creating Transactions...")

		self.app.showTransaction(win)
		self.about.info.setText("Creating Report...")
		self.about.update()
		sleep(2)
		self.app.showDecompte(win)
		self.win			= win
		self.dispatch	= dispatch
		
	def	mainLoop(self):
		self.about.close()
		self.about.info.setText("")
		self.win.show()
		ret = self.app.exec()

		self.app.conn.close()
		exit( ret )
