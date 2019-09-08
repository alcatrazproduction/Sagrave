from decXel 					import	decXel
from decPdf					import	decPdf

class dispatcher:
	def __init__(self, theWin, theApp, theConn):
		self.win		= theWin
		self.app		= theApp
		self.conn	= theConn
		self.Xcel		= decXel(theWin, theConn)
		self.Pdf		= decPdf(theWin, theConn)
		
	def	dateDecompte(self):
		self.app.showDecompte(self.win)
		
	def	dateTransaction(self):
		self.app.showTransaction(self.win)
		
	def	createExcel(self):
		self.Xcel.showDecompte(self.win)
		
	def	createPdf(self):
		self.Pdf.showDecompte()
		
	def 	setCards(self,  theCards):
		self.cards	= theCards
		
	def	editKey(self, item):
		self.cards.editCards()
	
	def 	setAbout(self,  theAbout):
		self.about	= theAbout
		
	def	doAbout(self):
		self.about.setModal( True )
		self.about.show()
