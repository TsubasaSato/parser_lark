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

def getattr_get_var(tree):
    #getattrが来ると思われる部分に配置
    print(tree)
    if len(tree.children)>1 and tree.children[0].data=="getattr":
        #getattrが続く場合
        data=getattr_get_var(tree.children[0])
        data.append(tree.children[1])
        return data
    else:
        data=[]
        data.append(tree.children[0])
        data.append(tree.children[1])
        return data    
        
class RyuToP4Transformer(Transformer):
    
    #変数宣言
    def expr_stmt(self,args):
        print("-----Start-------")
        print(args)
        #Tokenの名前取得方法
        print("len:",len(args))
        print(args[0].children)
        print(args[0].children[0])
        """
        if args[0].data=="var":
            #辞書のキーに登録
            if args[1].data=="var":
                pass
            elif args[1].data=="getattr":
                print(getattr_get_var(args[1]))
            elif args[1].data=="funccall":
                pass
            elif args[1].data=="list":
                pass
            else:
                pass
        print("-----Finished-----")
        """
        #print(RyuToP4Transformer(visit_tokens=True).transform(Tree("expr_stmt",args)))

