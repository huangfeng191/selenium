from main.utils.exception import UnrealizedException

from main.utils.time import getToday_s
import copy

#  提供 解析对象的功能
class ParseMethod():
    def today_str(self,*args,**kwargs):
        return getToday_s()

    def __getitem__(self, item):
        if item=="today_str":
            return self.today_str
        else:
            raise UnrealizedException()

class ParseCommObj():
    '''
     _tp 存在时 需要被解析,
     支持递归

    '''
    key="_tp"
    def __init__(self,base_obj,inplace=True,parse=True):
       self.base_obj= base_obj
       self.parsed=None
       self.inplace=inplace
       if parse:
           self.parse()
    def _parse(self,obj):
        for k,v in obj.items():
            if type(v)==dict and v.get(self.key):
                obj[k]=ParseMethod()[v[self.key]](**v)
            elif  type(v)==dict :
                self._parse(v)
        return self.parsed
    def parse(self):
        if not self.inplace:
            self.parsed=copy.deepcopy(self.base_obj)
        else:
            self.parsed=self.base_obj
        return self._parse(self.parsed)
    def get_parsed(self):
        return self.parsed




