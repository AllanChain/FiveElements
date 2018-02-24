#coding:utf-8
import struct
from FEcon import *
from pprint import pprint
size=struct.calcsize(pattern)

def read_db():
    stra_dict={}
    with open('Strategy/data.db','rb') as f:
        str2=f.read(size)
        while str2:
            name,*pose2=struct.unpack(pattern,str2)
            pose2=list(map(lambda x:divmod(x,32),pose2))
            #print(pose2)
            name=(name.decode()).replace('\x00','')
            str2=f.read(size)
            stra_dict[name]=pose2
    pprint(stra_dict)
    return stra_dict
def write_db(stra_dict):
    with open('Strategy/data.db','wb') as f:
        for name,poses in stra_dict.items():
            pose2=list(map(lambda x:(x[0]<<5)+x[1],poses))
            buffers=struct.pack(pattern,name.encode(),*pose2)
            f.write(buffers)
if __name__=='__main__':
    stra_dict=read_db()
    #del stra_dict[list(stra_dict.keys())[0]]
    write_db(stra_dict)
