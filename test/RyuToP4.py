from lark import Tree, Transformer
"""
class Environment():

    def __init__(self):
        self.var=dict()
        
    def set(self,key,value):
        self.var[key]=value

    def get(self,key):
        return self.var[key]
"""
class RyuToP4Transformer(Transformer):
    
    def expr_stmt(self,args):
        print(args.pretty())
        print(args)
