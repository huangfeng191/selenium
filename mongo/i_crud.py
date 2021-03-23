# -*- coding: utf-8 -*-

class ICRUD:
  
  def test_connect(self):
    raise NotImplementedError()
  
  @property
  def database(self):
    raise NotImplementedError()

  @property
  def db(self):
    raise NotImplementedError()
  
  @property
  def coll(self):
    raise NotImplementedError()

  def columns(self):
    raise NotImplementedError()
  
  def distinct(self, condition=None,fields=None, order=None,_sort=None ):
       raise NotImplementedError()
  
  def exists(self, _id):
    raise NotImplementedError()
  
  def get(self, _id):
    raise NotImplementedError()
    
  def index(self, indexes=None):
    raise NotImplementedError()
  
  def delete(self, _id=None,record=None,_direct=False, multi=False,*args, **kwArgs):
    raise NotImplementedError()
  
  def indexing(self, *argv, **kwArgs):
    raise NotImplementedError()
  
  '''
    @param module - 注入目标
    @parma field  - 注入目标字段
    @param id_key - 注入参考字段
  '''
  def inject(self, module, field, id_key, deleteCascade=False):
    raise NotImplementedError()
  
  '''
    数据验证接口
  '''
  def validate(self,action=None,_id=None,record=None,*args, **kwArgs):
      raise NotImplementedError()
  
  def on_delete(self, _id):
    pass
   
  def on_insert(self, _id, obj):
    pass
  
  def on_update(self, _id, obj, old):
    pass
  
  def on_upsert(self, _id, obj, old):
    pass
  
  def upsert(self,_id=None, _query=None,_changed=True, _upsert=False, _direct=False, _multi=False, _insert=True,_action=None, *args, **kwArgs):
    raise NotImplementedError()
  
  def query(self, conditions = None):
    raise NotImplementedError()
  
  def sort(self, order=None):
    raise NotImplementedError()
  
  def items(self, size=None, index=None, conditions = None, order=None, fields=None, query=None, _sort=None, *args, **kwArgs):
    raise NotImplementedError()

  def group(self,key, condition, initial, reduce, finalize=None):  # @ReservedAssignment
    raise NotImplementedError()
  
  
  def aggregate(self,count=True,index=None,size=None,conditions=None,groups=None,aggregate=None,order=None,fields=None,unwind=None, *args, **kwArgs):
    raise NotImplementedError()

  def count(self,conditions = None, query=None, *args, **kwArgs):
    raise NotImplementedError()