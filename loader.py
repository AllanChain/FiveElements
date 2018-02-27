#coding:utf-8
import struct
from pprint import pprint

def init(option):
    global size,pattern,file_name
    global opt
    opt=option
    if opt =='place':
        pattern='21s'+'h'*6
    elif opt=='color':
        pattern='21s'+'H'*18
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

def stra_to_color(stra_dict):
    new_dict={}
    attrs='金水木火土王'
    for name,poses in stra_dict.items():
        sty={}
        for i in range(6):
            attr=attrs[i]
            pose=poses[i*3:i*3+3]
            new_pose=tuple(zip(*pose))
            sty[attr]=new_pose
        new_dict[name]=sty
    return new_dict
def color_to_stra(stys):
    new_dict={}
    for name,sty in stys.items():
        pose=[]
        for color in sty.values():
            pose+=list(zip(*color))
        new_dict[name]=pose
    return new_dict

default_place={'默认': [(18, 19), (20, 21), (22, 23), (24, 25), (16, 17), (26, 27)]}
default_color={'defalt':{
    u'金':((200,200,100),(255,255,0)),
    u'水':((0,255,255),(0,0,180)),
    u'木':((50,255,175),(0,200,0)),
    u'火':((255,175,50),(200,0,0)),
    u'土':((200,175,150),(210,147,84)),
    u'王':((255,50,100),(0,200,0)),
    }}

if __name__=='__main__':
    init('place')
    #del stra_dict[list(stra_dict.keys())[0]]
    #write_db(stra_dict)
    if opt=='place':
        write_db(default_place)
        stra_dict=read_db()
    if opt=='color':
        write_db(color_to_stra(default_color))
        stra_dict=read_db()
        pprint(stra_to_color(stra_dict))
