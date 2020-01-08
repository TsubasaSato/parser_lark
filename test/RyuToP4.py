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
    
    #変数宣言
    def expr_stmt(self,args):
        print(args[0].data,args[0].children)
        print(args[0].data,args[1].children)
        #Tokenの名前取得方法
        print("len:",len(args))
        print("--var---args[0].children-----")
        print(args[0].children[0])
        print("--same node in var level---args[0].children-----")
        print(args[1].children[0])
        print("------Finished------")

        #print(RyuToP4Transformer(visit_tokens=True).transform(Tree("expr_stmt",args)))

