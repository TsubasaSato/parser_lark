from lark import Tree, Transformer
import copy
    
def check_same_list(token_list,normal_list):
    if len(token_list)!=len(normal_list):
        return False
    if type(token_list)==type(dict()):
        if not check_same_list(token_list.keys(),normal_list.keys()):
            return False
        elif not check_same_list(token_list.values(),normal_list.values()):
            return False
    else:
        for x in range(len(normal_list)):
            if type(token_list[x])==type(list()):
                if not check_same_list(token_list[x],normal_list[x]):
                    return False
            else:
                if token_list[x]!=normal_list[x]:
                    return False
    return True

class Message():
    entries=dict()
    pkt_out=list()
    src_inst="""    {inst}\n"""
    src_1="""if ({match}) {{\n    {inst}\n    }}\n"""
    src_2="""else if ({match}) {{\n    {inst}\n    }}\n"""
    p4src_f=[]
    
    
    def set_pktout(self,act,data):
        pass
    def get_pktout_code(self):
        pass
    def set_entry(self,table_id,priority,match,instructions):
        if len(match)>1:
            match=[" && ".join(match)]
        if table_id in self.entries:
            self.entries[table_id].append([int(priority),match,instructions])
        else:
            self.entries[table_id]=list()
            self.entries[table_id].append([int(priority),match,instructions])
    def get_code(self):
        table_ids=self.entries.keys()
        for x in table_ids:
            self.entries[x].sort(key=lambda x:x[0],reverse=True)
            count=1
            for y in self.entries[x]:
                #matchが空ならif文を作成しない
                if y[1]:
                    if count==1:
                        # formatの実引数をデバッグ
                        self.p4src_f.append(self.src_1.format(match=y[1][0],inst=y[2][0]))
                    else:
                        self.p4src_f.append(self.src_2.format(match=y[1][0],inst=y[2][0]))
                else:
                    self.p4src_f.append(self.src_inst.format(inst=y[2][0]))
                count=count+1
        return self.p4src_f

def get_p4src_pktout(_vars,actions,data):
    eth_reg="bit<48> eth_dst=hdr.ethernet.dstAddr;\n    bit<48> eth_src=hdr.ethernet.srcAddr;\n"
    ip_reg="bit<32> ipv4_dst=hdr.ipv4.dstAddr;\n    bit<32> ipv4_src=hdr.ipv4.srcAddr;\n"
    tcp_reg="bit<16> tcp_dst=hdr.tcp.dstPort;\n    bit<16> tcp_src=hdr.tcp.srcPort;\n"
    
    ethernet={
        "dst":"hdr.ethernet.dstAddr",
        "src":"hdr.ethernet.srcAddr",
        }
    ipv4={
        "dst":"hdr.ipv4.dstAddr",
        "src":"hdr.ipv4.srcAddr",
        }
    flags={
        "TCP_SYN":"hdr.tcp.syn = 1",
        "TCP_ACK":"hdr.tcp.ack = 1",
        }
    tcp={
        "src_port":"hdr.tcp.srcPort",
        "dst_port":"hdr.tcp.dstPort",
        "ack":"hdr.tcp.ackNo",
        "seq":"hdr.tcp.seqNo",
        "bits":flags,
        }
    proto={
        "ethernet":ethernet,
        "ipv4":ipv4,
        "tcp":tcp,
        }
    values={
        "ethernet":{"src":"eth_src","dst":"eth_dst"},
        "ipv4":{"src":"ipv4_src","dst":"ipv4_dst"},
        "tcp":{"src_port":"tcp_src","dst_port":"tcp_dst"},
        }
    p4src=[]
    p4src.append(actions)
    
    if data[-1]=="data":
        for x in data:
            if type(x)==type(list()):
                if x[1]=="ethernet":
                    p4src.append(eth_reg)
                elif x[1]=="ipv4":
                    p4src.append(ip_reg)
                elif x[1]=="tcp":
                    p4src.append(tcp_reg)
                dic=x[2][0]
                for y in dic.keys():
                    #変換可能な引数のみを変換する
                    if y in proto[x[1]]:
                        #辞書の値が変数なら変数を解析    
                        if type(dic[y])==type(list):
                            if y=="bits":
                                for z in dic[y]:
                                     p4src.append("{};\n".format(proto[x[1]][y][z][1]))
                            else:
                                #プロトコルを調べる
                                p=get_origin_name(_vars,dic[y][0])
                                print("protocol is :",p)
                                print("dic[y][1]:",dic[y][1])
                                print("values[p[4][0]][dic[y][1]]:",values[p[4][0]][dic[y][1]])
                                p4src.append("{} = {};\n".format(proto[x[1]][y],values[p[4][0]][dic[y][1]]))
                        else:
                            p4src.append("{} = {};\n".format(proto[x[1]][y],dic[y]))
    return p4src    
    
def get_p4src_packet(_vars,name):
    proto={
        "tcp":"hdr.tcp.isValid()",
        "ipv4":"hdr.ipv4.isValid()",
        "ethernet":"hdr.ethernet.isValid()",
        }
    flags={
        "TCP_SYN":"hdr.tcp.syn==1",
        "TCP_RST":"hdr.tcp.rst==1",
        }
    func={
        "get_protocol":proto,
        "has_flags":flags
        }
    p4src=[]
    dict_value=get_origin_name(_vars,name)
    pkt=["packet","Packet"]
    pkt_proto=["packet","Packet",[{"data":["msg","data"]}],"get_protocol"]
    pkt_has_flags=["packet","Packet",[{"data":["msg","data"]}],"get_protocol",
                   ["tcp","tcp"],"has_flags"]
    if check_same_list(dict_value[0:6],pkt_has_flags):
        #has_flags
        p4src.append(func[dict_value[5]][dict_value[7]])
    elif check_same_list(dict_value[0:4],pkt_proto):
        #pkt_proto
        p4src.append(proto[dict_value[4][0]])
    elif check_same_list(dict_value[0:2],pkt):
        #pkt
        pass
    return p4src

def get_p4src_mlist(_vars,name):
    #P4ソースコード
    p4src=[]
    eth_type={"0x0800":"hdr.ipv4.isValid()"}
    ip_proto={"6":"hdr.tcp.isValid()"}
    dict_value=get_origin_name(_vars,name)
    RyuToP4_key={
        "eth_type":eth_type,
        "ip_proto":ip_proto,
        "eth_dst":"hdr.ethernet.dstAddr",
        "eth_src":"hdr.ethernet.srcAddr",
        "ipv4_dst":"hdr.ipv4.dstAddr",
        "ipv4_src":"hdr.ipv4.srcAddr",
        "tcp_dst":"hdr.tcp.dstPort",
        "tcp_src":"hdr.tcp.srcPort",
    }
    OFPMatch=["ev","msg","datapath","ofproto_parser","OFPMatch"]
    #Ryuの固有関数:ev.msg.datapath.ofproto_parser.OFPMatch()であるか確認
    if check_same_list(dict_value[0:5],OFPMatch):
        if len(dict_value) > 5:
            data=dict_value[5]
            for x in data.keys():
                if x=="eth_type" or x == "ip_proto":
                    p4src.append(RyuToP4_key[x][data[x]])
                else:
                    p4src.append("{} == {}".format(RyuToP4_key[x],data[x]))
    return p4src

def get_p4src_alist(_vars,name):
    #OFPActionOutput:スイッチの出力ポートを決定するActionのみ可
    p4src=[]
    OFPActionOutput=["ev","msg","datapath","ofproto_parser","OFPActionOutput"]
    RyuToP4_key={
        "port":"standard_metadata.egress_spec",
        "in_port":"standard_metadata.ingress_port",
        }
    #Ryuの固有関数であるか確認
    dict_value=get_origin_name(_vars,name)
    if check_same_list(dict_value[0:5],OFPActionOutput):
        if len(dict_value)>5:
            data=dict_value[5:]
            if type(data[0])==type(dict()):
                data=data[0]
                for x in data.keys():
                    if x in RyuToP4_key:
                        #数字も文字列扱いされている可能性あり、要デバッグ
                        var=get_origin_name(_vars,[data[x].value])[-1]
                        if type(var)!=type(str()):
                            if var.value in RyuToP4_key:
                                p4src.append("{} = {}".format(RyuToP4_key[x],RyuToP4_key[var.value]))
                        else:
                            p4src.append("{} = {}".format(RyuToP4_key[x],var))
            else:
                #Packet-Inの処理を記述
                pass
    return p4src

def get_p4src_ilist(_vars,name):
    p4src=[]
    OFPInstGoto=["ev","msg","datapath","ofproto_parser","OFPInstructionGotoTable"]
    OFPInstActA=["ev","msg","datapath","ofproto_parser","OFPInstructionActions","ofproto","OFPIT_APPLY_ACTIONS"]
    OFPInstActW=["ev","msg","datapath","ofproto_parser","OFPInstructionActions","ofproto","OFPIT_WRITE_ACTIONS"]
    dict_value=get_origin_name(_vars,name)
    #Ryuの固有関数であるか確認
    if check_same_list(dict_value[0:5],OFPInstGoto):
        #FlowModで指定されたtableIDと同じ番号のエントリをここに配置
        p4src.append(dict_value[4])
        p4src.append(dict_value[5])
    elif check_same_list(dict_value[0:7],OFPInstActA) or check_same_list(dict_value[0:7],OFPInstActW):
        #Actionsをget_origin_nameしてActionの取得
        actions=get_p4src_alist(_vars,[dict_value[-1]])
        p4src.append(actions)
    return p4src

def get_origin_name(dic,name_list):
    #変数宣言された時の名前に変換、リスト化して出力、再帰
    names=copy.deepcopy(name_list)
    while names[0] in dic:
        names[0] = dic[names[0]]
        for x in names:
            if type(x) != type(list()):
                names[names.index(x)]=[x]
        names=sum(names,[])
    return names

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
            if x.children[1].data=="expr":
                arg_dict[x.children[0].children[0]]=[getattr_get_list(x.children[1].children[0]),
                                                     getattr_get_list(x.children[1].children[1])]
            elif x.children[1].data!="getattr":
                arg_dict[x.children[0].children[0]]=x.children[1].children[0]
            else:
                arg_dict[x.children[0].children[0]]=getattr_get_list(x.children[1])
        elif x.data=="funccall":
            arg_list=funccall_get_list(x)
        elif x.data=="subscript":
            item = x.children[0].children[0]
            item.type="NAME"
            item.value=item.value.strip("'")
            arg_list.append(item)
        elif x.data=="var":
            arg_list.append(x.children[0])
        else:
            arg_list.append(x.children[0])
    if arg_dict != dict():
        arg_list.append(arg_dict)
    return arg_list

def funccall_get_list(tree):
    #関数を呼び出して変数に代入する記述を入力、リストに入った辞書を出力
    object=getattr_get_list(tree.children[0])
    if len(tree.children)>1:
        #引数を取得
        object.append(arg_get_dict_list(tree.children[1]))
    return object

def send_msg(_vars,args_tree,_msg):
    code=dict()
    p4src=[]
    msg=[]
    FlowMod=["ev","msg","datapath","ofproto_parser","OFPFlowMod"]
    PacketOut=["ev","msg","datapath","ofproto_parser","OFPPacketOut"]
    
    if args_tree.children[0].data=="var":
        msg=get_origin_name(_vars,[args_tree.children[0].children[0]])
    elif args_tree.children[0].data=="funccall":
        msg=get_origin_name(_vars,funccall_get_list(args_tree.children[0]))
    if check_same_list(msg[0:5],FlowMod):
        t_id,p,m,i=msg[5]["table_id"],msg[5]["priority"],msg[5]["match"],msg[5]["instructions"]
        _msg.set_entry(t_id,p,get_p4src_mlist(_vars,[m]),get_p4src_ilist(_vars,[i]))
    elif check_same_list(msg[0:5],PacketOut):
        #PacketOutの記述
        print("data in send_msg")
        print(get_p4src_pktout(_vars,get_p4src_alist(_vars,[msg[5]["actions"]]),get_origin_name(_vars,[msg[5]["data"]])))
    
class RyuToP4Transformer(Transformer):
    env=dict()
    message=Message()
    #変数宣言
    
    def expr_stmt(self,args):
        print("-----Start in expr_stmt------")
        if args[0].data=="var":
            if args[1].data=="var":
                pass
            elif args[1].data=="getattr":
                self.env[args[0].children[0]]=getattr_get_list(args[1])
            elif args[1].data=="funccall":
                self.env[args[0].children[0]]=funccall_get_list(args[1])
            elif args[1].data=="list":
                self.env[args[0].children[0]]=funccall_get_list(args[1].children[0])
            elif args[1].data=="getitem":
                self.env[args[0].children[0]]=funccall_get_list(args[1])
            else:
                pass
        if "pkt_ethernet" in self.env:
            #print(get_origin_name(self.env,self.env["pkt_ethernet"]))
            pass
        if "pkt_in" in self.env:
            #print(get_origin_name(self.env,self.env["pkt_in"]))
            pass
        print("-----Finished in expr_stmt---")
    
    def funccall(self,args):
        #packet.Packet()とsend_msg()用に分けて考える
        #datapath.send_msgにしておく
        if args[0].children[1] =="send_msg":
            print("-----Start in funccall-------")
            send_msg(self.env,args[1],self.message)
        if args[0].children[1]=="add_protocol":
            print("add_protocol")
            self.env[args[0].children[0].children[0]].append(arg_get_dict_list(args[1]))
            print(self.env[args[0].children[0].children[0]])
        else:
            return Tree("funccall",args)
    def if_stmt(self,args):
        print("-----Start in if_stmt---")
        #リストにnotを入れる
        if args[0].data=="not":
            if args[0].children[0].data=="var":
                print(get_p4src_packet(self.env,[args[0].children[0].children[0]]))
        elif args[0].data=="funccall":
            print(get_p4src_packet(self.env,funccall_get_list(args[0])))
        elif args[0].data=="var":
            print(get_p4src_packet(self.env,[args[0].children[0]]))
        
        print("-----Finished in if_stmt---")
    def elif_stmt(self,args):
        print("-----Start in elif_stmt---")
        #リストにnotを入れる
        if args[0].data=="not":
            if args[0].children[0].data=="var":
                print(get_p4src_packet(self.env,[args[0].children[0].children[0]]))
        elif args[0].data=="funccall":
            print(get_p4src_packet(self.env,funccall_get_list(args[0])))
        elif args[0].data=="var":
            print(get_p4src_packet(self.env,[args[0].children[0]]))
        
        print("-----Finished in elif_stmt---")
    def get_alldicts(self):
        return self.env

    def get_dict(self,key):
        return self.env[key]
