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

class T(Transformer):
    def NAME(self,name):
        print(name)
        print(type(name))
    
    
class RyuToP4Transformer(Transformer):
    
    def __init__(self):
        self.vars=dict()
        
    #変数宣言
    def expr_stmt(self,args):
        print(args[0])
        print(args)
        #print(RyuToP4Transformer(visit_tokens=True).transform(Tree("expr_stmt",args)))
    def NAME(self,name):
        print(name)
