from main.page import Table
class RestTable(Table):
    def __init__(self,restUrl,titleBind,**kwargs):
        self.restUrl = restUrl
        self.titleBind = titleBind
        self.df = None

    def getDf(self, ):
        pass

    def save(self, ):
        pass

