import logging 
import os
from main import config
log_path=config.get("sys").get("log_path")
from main.utils.time import getToday_s

class FileLog():
   loggers={}
   debugger=True
   # debugger=False
   def __init__(self,name,sub_path=".",level=logging.INFO,today=False,formatter="'%(asctime)s:%(levelname)s:%(message)s"):
      self.name=os.path.splitext(name)[0]+"_"+getToday_s()+os.path.splitext(name)[1] if today else name
      self.path=os.path.join(os.getcwd(),log_path,sub_path)
      self.level=level
      if self.debugger:
         self.level=logging.DEBUG
      self.formatter=formatter
      self.sub_path_name=os.path.join(sub_path,self.name)
      self.init_log()
   def init_log(self):
      self.logger = self.loggers.get(self.sub_path_name)
      if not self.logger:
         logger=logging.getLogger(self.sub_path_name)
         logger.setLevel(self.level)
         if not os.path.exists(self.path): os.makedirs(self.path)
         file_handler=logging.FileHandler(os.path.join(self.path,self.name),encoding="utf-8")
         if self.formatter:
            formatter=logging.Formatter(self.formatter)
            file_handler.setFormatter(formatter)
         logger.addHandler(file_handler)

         if self.debugger:
            stream_handler=logging.StreamHandler()
            stream_formatter=logging.Formatter(f":%(asctime)s:{logging.BASIC_FORMAT}")
            stream_handler.setFormatter(stream_formatter)
            logger.addHandler(stream_handler)
         self.loggers[self.sub_path_name]=logger
         self.logger=logger




   
