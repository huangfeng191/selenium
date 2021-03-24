import json
from main.utils.exception import UnrealizedException

from main.page.service import treasure_industry,treasure_industry_detail

from main.page.util import ParseCommObj

# 支持的方法
class BindCurd():
    @staticmethod
    def get(item):
        if item=="industry":
            return treasure_industry
        if item == "industry_detail":
            return treasure_industry_detail


class SaveBase():
    def save(self):
        pass
    @classmethod
    def from_yarm(cls,**kwargs):
        kwargs=ParseCommObj(base_obj=kwargs).get_parsed()
        return cls(**kwargs)

class MongoSave(SaveBase):
    def __init__(self,df=None,data=None,unique_k=None,const=None,crud_nm=None,db=None,is_crud=True,**kwargs):
        self.data=data
        self.df=df
        self.unique_k=unique_k
        self.crud=BindCurd.get(crud_nm)if crud_nm else None
        self.db=db
        self.is_crud=is_crud
        self.const=const
    def _bind_const(self ,r):
        if self.const and r:
            r.update(self.const)

    def _crud_save(self):
        if self.unique_k:
            self.crud.delete(self.unique_k,multi=True)
        if not self.data:
            a= json.loads(self.df.to_json(orient="records"))
        else:
            a=self.data
        for r in a:
            self._bind_const(r)
            self.crud.upsert(**r)
    def save(self):
        if self.is_crud:
            self._crud_save()
        else:
            raise UnrealizedException()

class SaveFactory():
    @staticmethod
    def init( tp="mongo"):

        if tp=="mongo":
            saveBase=MongoSave
        else:
            raise UnrealizedException()
        return saveBase

