#coding:utf-8
import struct
from FEcon import *
from pprint import pprint
def init(opt):
    global size,pattern,file_name
    if opt in('place','color'):
        pattern='21s'+'h'*6
    elif opt=='record':
        pattern='21s'+'h'*11
    file_name=opt+'.fe'
    size=struct.calcsize(pattern)
def read_db():
    stra_dict={}
    with open('Strategy/'+file_name,'rb') as f:
        str2=f.read(size)
        while str2:
            name,*pose2=struct.unpack(pattern,str2)
            pose2=list(map(lambda x:divmod(x,256),pose2))
            #print(pose2)
            name=(name.decode()).replace('\x00','')
            str2=f.read(size)
            stra_dict[name]=pose2
    pprint(stra_dict)
    return stra_dict
def write_db(stra_dict):
    with open('Strategy/'+file_name,'wb') as f:
        for name,poses in stra_dict.items():
            pose2=list(map(lambda x:(x[0]<<8)+x[1],poses))
            buffers=struct.pack(pattern,name.encode(),*pose2)
            f.write(buffers)
def write_default_place():
    write_db({'默认': [(18, 19), (20, 21), (22, 23), (24, 25), (16, 17), (26, 27)]})
if __name__=='__main__':
    init('place')
    #del stra_dict[list(stra_dict.keys())[0]]
    #write_db(stra_dict)
    write_default_place()
    stra_dict=read_db()
