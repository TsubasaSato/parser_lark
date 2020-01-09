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
"""
class Match():
    eth_type
    eth_src
    eth_dst
    ip_proto
    ipv4_src
    ipv4_dst
    tcp_src
    tcp_dst
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
    #リストに入った辞書を返す
    arg_list=[]
    arg_dict=dict()
    for x in tree.children:
        if x.data=="getattr":
            arg_list.append(getattr_get_list(x))
        elif x.data=="argvalue":
            arg_dict[x.children[0].children[0]]=x.children[1].children[0]
    arg_list.append(arg_dict)
    return arg_list

def funccall_get_list(tree):
    print(tree)
    print(tree.children)
    data=getattr_get_list(tree.children[0])
    sub=arg_get_dict_list(tree.children[1])
    print(data)
    print(sub)
    
class RyuToP4Transformer(Transformer):
    
    #変数宣言
    def expr_stmt(self,args):
        print("-----Start-------")
        if args[0].data=="var":
            #辞書のキーに登録
            if args[1].data=="var":
                pass
            elif args[1].data=="getattr":
                #print(getattr_get_list(args[1]))
                pass
            elif args[1].data=="funccall":
                print("---args---")
                print(args)
                print("--funccall_get_list--")
                print(funccall_get_list(args[1]))
            elif args[1].data=="list":
                pass
            else:
                pass
        print("-----Finished-----")
        
        #print(RyuToP4Transformer(visit_tokens=True).transform(Tree("expr_stmt",args)))

