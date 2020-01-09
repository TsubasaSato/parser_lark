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

def getattr_get_list(tree):
    """
    getattrが来る部分に配置
    datapath = ev.msg.datapathを
    [[Tree(var, [Token(NAME, 'ev')]), Token(NAME, 'msg'), Token(NAME, 'datapath')]]
    Tokenのリストで返す。Tokenオブジェクトはそのままプリントすれば中身の値が出力される。
    """
    if len(tree.children)>1 and tree.children[0].data=="getattr":
        #getattrが続く場合
        data=getattr_get_list(tree.children[0])
        data.append(tree.children[1])
        return data
    else:
        data=[]
        data.append(tree.children[0].children[0])
        data.append(tree.children[1])
        return data
def arg_get_dict_list(tree):
    #argumentsを入力、リストに入った辞書を出力
    arg_list=[]
    arg_dict=dict()
    for x in tree.children:
        if x.data=="getattr":
            arg_list.append(getattr_get_list(x))
        elif x.data=="argvalue":
            arg_dict[x.children[0].children[0]]=x.children[1].children[0]
        elif x.data=="funccall":
            arg_list=funccall_get_list(x)
    if arg_dict != dict():
        arg_list.append(arg_dict)
    return arg_list

def funccall_get_list(tree):
    #関数を呼び出して変数に代入する記述を入力、リストに入った辞書を出力
    data=getattr_get_list(tree.children[0])
    if len(tree.children)>1:
        data.append(arg_get_dict_list(tree.children[1]))
    return data
    
class RyuToP4Transformer(Transformer):
    env=dict()
    
    #変数宣言
    """
    def expr_stmt(self,args):
        print("-----Start-------")
        if args[0].data=="var":
            if args[1].data=="var":
                pass
            elif args[1].data=="getattr":
                self.env[args[0].children[0]]=getattr_get_list(args[1])
            elif args[1].data=="funccall":
                self.env[args[0].children[0]]=funccall_get_list(args[1])
            elif args[1].data=="list":
                self.env[args[0].children[0]]=funccall_get_list(args[1].children[0])
            else:
                pass
        print("-----Finished-----")
    """
    def funccall(self,args):
        if args[0].children[1] =="send_msg":
            print("-----Start-------")
            print(args[1])
            print(Tree("Funccall",args).pretty())
            print("-----Finished-----")
        else:
            return Tree("funccall",args[0])
        
        
    def dict_print(self):
        print(self.env)
        #print(RyuToP4Transformer(visit_tokens=True).transform(Tree("expr_stmt",args)))

