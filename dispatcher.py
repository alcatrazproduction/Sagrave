#!/usr/bin/env python3
#######################################################################################################
#	Dispatcher for the event in the App																						#
#	Do all the events stuff																										#
#	Creator:		Yves Huguenin																									#
#	Date:			06.09.2019																										#
#	Version:		0.1																												#
#																																		#
#######################################################################################################

from decXel 				import	decXel
from decPdf					import	decPdf

class dispatcher:
####################################################################################################
#																																	#
#																																	#
####################################################################################################

	def __init__(self, theWin, theApp, theConn):
		self.win		= theWin
		self.app		= theApp
		self.conn	= theConn
		self.Xcel		= decXel(theWin, theConn)
		self.Pdf		= decPdf(theWin, theConn)
		
####################################################################################################
#																																	#
#																																	#
####################################################################################################

	def dateDecompte(self):
		self.app.showDecompte(self.win)
		
####################################################################################################
#																																	#
#																																	#
####################################################################################################

	def dateTransaction(self):
		self.app.showTransaction(self.win)
		
####################################################################################################
#																																	#
#																																	#
####################################################################################################

	def createExcel(self):
		self.Xcel.showDecompte(self.win)
		
####################################################################################################
#																																	#
#																																	#
####################################################################################################

	def createPdf(self):
		self.Pdf.showDecompte()
		
####################################################################################################
#																																	#
#																																	#
####################################################################################################

	def  setCards(self,  theCards):
		self.cards	= theCards
		
####################################################################################################
#																																	#
#																																	#
####################################################################################################

	def editKey(self, item):
		self.cards.editCards()
	
####################################################################################################
#																																	#
#																																	#
####################################################################################################

	def  setAbout(self,  theAbout):
		self.about	= theAbout
		
####################################################################################################
#																																	#
#																																	#
####################################################################################################

	def doAbout(self):
		self.about.setModal( True )
		self.about.show()
		
####################################################################################################
#																																	#
#																																	#
####################################################################################################

	def resizeWindow(self):
		win	= self.win
		size	= win.size()
		msize	= 20
		tsize	= msize + 20
		vsize	= tsize + 20
		hsize	= 20
		
		win.tabs.setFixedWidth( size.width() )
		win.tabs.setFixedHeight( size.height() - msize )
		
		win.p_cards.setFixedWidth( size.width() - hsize )
		win.p_cards.setFixedHeight( size.height() - tsize )
		win.v_cards.setFixedWidth( size.width() - hsize )
		win.v_cards.setFixedHeight( size.height() - tsize )

		win.p_transactions.setFixedWidth( size.width() - hsize )
		win.p_transactions.setFixedHeight( size.height() - vsize )
		win.v_transactions.setFixedWidth( size.width() - hsize )
		win.v_transactions.setFixedHeight( size.height() - vsize )
		win.vl_transactions.update()
				

		win.p_decomptes.setFixedWidth( size.width() - hsize )
		win.p_decomptes.setFixedHeight( size.height() - vsize)
		win.t_decompte.setFixedWidth( size.width() - hsize )
		win.t_decompte.setFixedHeight( size.height() - vsize)
		
