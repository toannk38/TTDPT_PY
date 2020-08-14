import pandas as pd
from collections import Counter

def generate(bin_code = '', char = [],total = 0, _dict ={}):
    if len(char) == 1:
        _dict[char[0][1]] = bin_code
        return
    count = char[0][0]
    i = 1
    while True:
        left = count + char[i][0]
        right = total - left
        if left*2 > total:
                break
        count += char[i][0]
        i+=1
    generate(bin_code+'0',char[:i],count,_dict)
    generate(bin_code+'1',char[i:],total-count,_dict)


def encode(inp,out):
    #read data
    with open(inp) as f:
        content = f.readlines()
    content = ''.join(content)
    if content == '':
        return

    bits_data = len(content)*8

    #character statistic
    count = Counter(content)

    total = sum(count.values())
    char = [x[::-1] for x in list(count.items())]

    #sort
    char.sort(reverse=True)

    #create dictionary
    _dict = dict()
    generate('',char,total,_dict)

    #encode
    code = ''
    for c in content:
        code += _dict[c]

    file = open(out, 'w')
    file.write(code)
    file.close()

    bits_compressed = len(code)

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

    return bits_data,bits_compressed

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

def sf(names):
    res = []
    for name in names:
        data_path = 'Data/' + name + '.txt'
        encode_path = 'Compressed/' + name + '_SF.txt'
        decode_path = 'Decompressed/' + name + '_SF.txt'
        bits = encode(data_path, encode_path)
        decode(encode_path, decode_path)
        res.append(bits)
    return res