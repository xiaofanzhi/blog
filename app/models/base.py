from  app.ext import db
from sqlalchemy import Column, Integer
from datetime import datetime

class Base(db.Model):
    __abstract__=True



    def set_attrs(self,arrts_dict):
        for k,v in arrts_dict.items():
            if hasattr(self,k) and k!='id':
                setattr(self,k,v)