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
        return name
    
    
class RyuToP4Transformer(Transformer):
    
    def __init__(self):
        self.vars=dict()
        
    #変数宣言
    def expr_stmt(self,args):
        #Token内の名前が取得可
        print(T(visit_tokens=True).transform(args[0]))
        print(args[0])
        print(args)
        #print(RyuToP4Transformer(visit_tokens=True).transform(Tree("expr_stmt",args)))
