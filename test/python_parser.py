#
# This example demonstrates usage of the included Python grammars
#

import sys
import os, os.path
from io import open
import glob, time

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

# python_parser2 = Lark.open('python2.lark', parser='lalr', **kwargs)
python_parser3 = Lark.open('python3.lark',parser='lalr', **kwargs)
# python_parser2_earley = Lark.open('python2.lark', parser='earley', lexer='standard', **kwargs)


def _read(fn, *args):
    kwargs = {'encoding': 'iso-8859-1'}
    with open(fn, *args, **kwargs) as f:
        return f.read()

def _get_lib_path():
    if os.name == 'nt':
        if 'PyPy' in sys.version:
            return os.path.join(sys.prefix, 'lib-python', sys.winver)
        else:
            return os.path.join(sys.prefix, 'Lib')
    else:
        return [x for x in sys.path if x.endswith('%s.%s' % sys.version_info[:2])][0]

def test_python_lib():

    path = _get_lib_path()

    start = time.time()
    files = glob.glob(path+'/*.py')
    for f in files:
        print( f )
        try:
            # print list(python_parser.lex(_read(os.path.join(path, f)) + '\n'))
            try:
                xrange
            except NameError:
                python_parser3.parse(_read(os.path.join(path, f)) + '\n')
            else:
                python_parser2.parse(_read(os.path.join(path, f)) + '\n')
        except:
            print ('At %s' % f)
            raise

    end = time.time()
    print( "test_python_lib (%d files), time: %s secs"%(len(files), end-start) )

def test_earley_equals_lalr():
    path = _get_lib_path()

    files = glob.glob(path+'/*.py')
    for f in files:
        print( f )
        tree1 = python_parser2.parse(_read(os.path.join(path, f)) + '\n')
        tree2 = python_parser2_earley.parse(_read(os.path.join(path, f)) + '\n')
        assert tree1 == tree2

# このクラスはTreeクラスの木構造をtopdownに検索できるように追加実装したクラスである
class Tree_2(Tree):
    # Treeクラスと同様のコンストラクタ
    def __init__(self,data,children,meta=None):
        super().__init__(data,children,meta)
        
    def find_pred_topdown(self, pred):
        "Find all nodes where pred(tree) == True with topdown"
        return filter(pred, self.iter_subtrees_topdown())
    
    def find_data_topdown(self, data):
        "Find all nodes where tree.data == data with topdown"
        return self.find_pred_topdown(lambda t: t.data == data)
    
if __name__ == '__main__':
    # test_python_lib()
    # test_earley_equals_lalr()
    tree=python_parser3.parse(_read(sys.argv[1]) + '\n')
    #tree=Tree_2(pre_tree.data,pre_tree.children,pre_tree._meta)
    #print("----------Tree2().pretty()-----")
    #print(Tree_2("decorated",list(tree.find_data_topdown("decorated"))).pretty())
    #print("----------transform(tree)------")
    data=list(tree.find_data("decorated"))
    #Switch_featuredハンドラ
    T=RyuToP4Transformer()
    T.transform(list(data[0].find_data("funcdef"))[0])
    print("---------------{}----------------".format(len(data)))
    #Packet_inハンドラ
    T.transform(list(data[1].find_data("funcdef"))[0])
    #RyuToP4Transformer().transform(tree)
    T.dict_print()
    
