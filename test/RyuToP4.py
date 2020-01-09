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
    object=[]
    if (tree[0].data=="getattr"):
        getattr_get_var(tree.children)
        if 
    elif (tree[0].data=="var"):
        object.append(tree[0].children[0])
        object.append(tree[1].data)
    return object

def getattr_get_var(tree):
    #getattrが来ると思われる部分に配置
    if (len(tree[0].children)>1,tree[0].children[0].data=="getattr"):
        #getattrが続く場合
        data=getattr_get_var(tree[0].children[0])
        data.append(tree[0].children[1].data)
        return data
    else:
        data=[]
        data.append(tree[0].children[0])
        data.append(tree[0].children[1].data)
        return data    
        
class RyuToP4Transformer(Transformer):
    
    #変数宣言
    def expr_stmt(self,args):
        print("-----Start-------")
        print(args[0].data,args[0].children)
        print(args[0].data,args[1].children)
        #Tokenの名前取得方法
        print("len:",len(args))
        print(getattr_get_var(args))
        print("-----Finished-----")
        """
        if (args[0].data=="var"):
            #辞書のキーに登録
            if (args[1].data=="var"):
                #辞書の値に登録
            elif (args[1].data=="getattr"):
                
            elif (args[1].data=="funccall"):
                #
            elif (args[1].data=="list"):
                #
            else:
                #エラー
        """

        #print(RyuToP4Transformer(visit_tokens=True).transform(Tree("expr_stmt",args)))

