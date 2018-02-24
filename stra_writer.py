import struct
from FEcon import *
from random import randint
def get_name():
    name='默认'+str(rd())
    print(name)
    return bytes(name.encode())
def rd():
    return randint(0,17)
#poses=[(rd()<<5)+rd() for i in range(chessnum)]
poses=[32*18+19,32*20+21,32*22+23,32*24+25,32*16+17,32*26+27]
strs=struct.pack(pattern,get_name(),*poses)
print(strs)
print(struct.calcsize(pattern))
with open('Strategy/data.db','wb')as f:
    f.write(strs)
