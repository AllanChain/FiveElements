import loader
def init(mod):
    global stra_dict
    loader.init(mod)
    stra_dict=loader.read_db()
def add(name,base):
    items=list(stra_dict.keys())
    if not name in items and base in items:
        stra_dict[name]=stra_dict[base].copy()
    else:
        raise ValueError('name in items or base does not in items')
def delete(name):
    if name in list(stra_dict.keys()):
        del stra_dict[name]
        print(stra_dict)
    else:
        raise ValueError('name does not in items')
def rename(dest,orig):
    add(dest,orig)
    delete(orig)
def save():
    print(stra_dict)
    loader.write_db(stra_dict)
        
