# -*- coding:UTF-8 -*-
from Test import Caller
import sys
''' 
y ex           壮              天赐           yj tiantai     yj hangzhou   广儿          吴虎
13738624333    17855338221    17855338336    15906764932    13588235607   17855337209   18756802586
'''
phonebook = {'y':'17855336108','yex':'13738624333','壮':'17855338221','天赐':'17855338336','yjtt':'15906764932','yyhz':'13588235607','广儿':'18269875902','吴虎':'18756802586','阮奇':'17855337639'}
def test(argv):
    number = 1000
    tel = int(phonebook[argv[1]])
    print(argv,argv[1],tel)
    Caller(tel, number)

if __name__ == '__main__' :
    test(sys.argv)
