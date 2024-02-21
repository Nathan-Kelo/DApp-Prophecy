def simple_hash(string):
    if string is None:
        return
    tmp=0
    for i in string:
        tmp=tmp+ord(i)
        tmp=tmp^(tmp*31)
        tmp=tmp%(2**32)
    return tmp
    