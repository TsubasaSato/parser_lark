#
# This example demonstrates usage of the included Python grammars
#

import sys
import os, os.path
from io import open
import glob, time, subprocess

from RyuToP4 import RyuToP4Transformer

from lark import Lark,Tree,Visitor
from lark.indenter import Indenter

# __path__ = os.path.dirname(__file__)

class PythonIndenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4 # Original value was 8 !!

kwargs = dict(rel_to=__file__, postlex=PythonIndenter(), start='file_input')

python_parser3 = Lark.open('python3.lark',parser='lalr', **kwargs)


def _read(fn, *args):
    kwargs = {'encoding': 'iso-8859-1'}
    with open(fn, *args, **kwargs) as f:
        return f.read()
    
import subprocess


def run_and_capture(cmd):
    '''
    :param cmd: str 実行するコマンド.
    :rtype: str
    :return: 標準出力.
    '''
    # ここでプロセスが (非同期に) 開始する.
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    buf = []
    a=[b'loading app TcpSyn_comment.py\n', b'loading app ryu.controller.ofp_handler\n', b'instantiating app TcpSyn_comment.py of TCPSYN13\n', b'instantiating app ryu.controller.ofp_handler of OFPHandler\n', b'BRICK TCPSYN13\n', b'  CONSUMES EventOFPPacketIn\n', b'  CONSUMES EventOFPSwitchFeatures\n', b'BRICK ofp_event\n', b"  PROVIDES EventOFPPacketIn TO {'TCPSYN13': {'main'}}\n", b"  PROVIDES EventOFPSwitchFeatures TO {'TCPSYN13': {'config'}}\n", b'  CONSUMES EventOFPEchoReply\n', b'  CONSUMES EventOFPEchoRequest\n', b'  CONSUMES EventOFPErrorMsg\n', b'  CONSUMES EventOFPHello\n', b'  CONSUMES EventOFPPortDescStatsReply\n', b'  CONSUMES EventOFPPortStatus\n', b'  CONSUMES EventOFPSwitchFeatures\n']


    while True:
        # バッファから1行読み込む.
        line = proc.stdout.readline()
        buf.append(line)
        print(buf)

        # バッファが空 + プロセス終了.
        if buf==a:
            break
    proc.terminate()
    print("terminate()")
    
if __name__=='__main__':
    
    tree=python_parser3.parse(_read(sys.argv[1]) + '\n')

    T=RyuToP4Transformer()
    T.transform(tree)

    code=T.message.get_code()
    T=None
    p4src=_read("./P4src.p4")
    with open(r"./src/p4src.p4","w") as f:
        f.write(p4src % code)
    subprocess.call(["p4c","--target","bmv2","--arch","v1model","./src/p4src.p4"])
    run_and_capture(["simple_switch","--log-file","p4src-log","-i","1@enp1s0f0","-i","2@enp1s0f1","p4src.json"])
