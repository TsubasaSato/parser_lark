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
    a=[b'Calling target program-options parser\n', b'Adding interface enp1s0f0 as port 1\n', b'Adding interface enp1s0f1 as port 2\n']

    while True:
        # バッファから1行読み込む.
        line = proc.stdout.readline()
        buf.append(line)

        # バッファが空 + プロセス終了.
        if buf==a:
            break
    proc.terminate()
    
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
