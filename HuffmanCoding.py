import pandas as pd
from collections import Counter
from copy import deepcopy as cp

import heapq

class Node:
    def __init__(self,freq = 0,p = ''):
        self.freq = freq
        self.p = p
    def __lt__(self,other):
        return self.freq < other.freq

def generate(bin_code = '', node = Node() , _dict ={}):

    #if p is leaf, p[1] is symbol, p[0] is frequency of p[1]
    if isinstance(node.p,str):
        _dict[node.p] = bin_code
    else:
        #generate binary code for children node of p

        generate(bin_code+'0', node.p[0],_dict)
        generate(bin_code+'1', node.p[1],_dict)


def encode(inp,out):
    #read data
    with open(inp) as f:
        content = f.readlines()
    content = ''.join(content)
    if content == '':
        return
    #character statistic
    count = Counter(content)

    total = sum(count.values())

    #char is list of frequency and symbol [(freq,sym)]
    char = [Node(x[1],x[0]) for x in list(count.items())]

    #transform to heap
    heapq.heapify(char)
    while len(char) > 1:
        #pop two
        a = heapq.heappop(char)
        b = heapq.heappop(char)

        #create parent node for a and b
        p = Node(a.freq+b.freq,(a,b))
        #push parent node to heap
        heapq.heappush(char,p)

    #create dictionary
    _dict = dict()
    generate(bin_code = '',node = char[0],_dict = _dict)
    #encode
    code = ''
    for c in content:
        code += _dict[c]

    file = open(out, 'w')
    file.write(code)
    file.close()

    #decode dictionary
    dict_path = out[:-4] + '_dict.csv'

    keys = []
    values = []
    for key in _dict:
        keys.append(_dict[key])
        values.append(key)
    encoded = {'keys': list(keys), 'values': list(values)}
    df = pd.DataFrame(encoded)
    df.to_csv(dict_path, index=False)


def decode(inp, out):
    dict_path = inp[:-4] + '_dict.csv'
    # read dictionary
    df = pd.read_csv(dict_path,dtype=str)
    keys = list(df['keys'])
    values = list(df['values'])
    _dict = dict(zip(keys,values))
    #read data
    with open(inp) as f:
        data = f.readlines()
    data = ''.join(data)

    #decode
    output = ''
    s = ''

    for c in data:
        if s+c not in _dict:
            s+=c
        else:
            output+=_dict[s+c]
            s = ''

    # save decoded data
    file = open(out, 'w')
    file.write(output)
    file.close()


def hc(names):
    for name in names:
        data_path = 'Data/' + name + '.txt'
        encode_path = 'Compressed/' + name + '_HC.txt'
        decode_path = 'Decompressed/' + name + '_HC.txt'
        encode(data_path, encode_path)
        decode(encode_path, decode_path)
