#!/usr/bin/python
#-*- coding: utf-8 -*-

from main.utils import yaml_loader

TableConfig=yaml_loader("./table.yaml")

# class OtherFieldRule():
#     def __init__(self,tp):
#         self.tp=tp







class Table:
    def __init__(self):
        pass
    def start(self,):
        '''
        开始获取数据
        :return:
        '''
        pass
    def get_df(self, ):
        pass

    def save(self, ):
        pass
    @classmethod
    def from_yaml(cls,name,tp):
        config=TableConfig[name][tp]
        return cls(**config)


class PageFactory:
    def __init__(self,source="yaml"):
        self.source= source


    def getTable(self, name,tp):
        if self.source=="yaml":
            if tp=="rest":
                table=RestTable.from_yaml(name,tp)
            elif tp=="selenium":
                table=SeleniumTable.from_yaml(name,tp)
        return table



from main.page.rest import RestTable
from main.page.selenium import SeleniumTable








