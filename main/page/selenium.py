from main.page import Table
class SeleniumTable(Table):
    def __init__(self,id,nextButton,url,**kwargs):
        self.id = id
        self.nextButton = nextButton
        self.df = None
        self.url = url

    def getDf(self, ):
        pass

    def save(self, ):
        pass