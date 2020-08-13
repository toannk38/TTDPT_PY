import pandas as pd

def encode(inp,out):
    #read data
    with open(inp) as f:
        content = f.readlines()
    content = ''.join(content)

    if content == '':
        return

    #initial
    symbols = list(set(list(content)))
    _dict = dict(zip(symbols,list(range(len(symbols)))))
    count = len(symbols)
    compressed = []
    s = ''

    for c in content:
        if s+c in _dict:
            s = s + c
            continue
        #if s+ c not in en_dict
        compressed.append(_dict[s])
        _dict[s+c]= count
        count += 1
        s = c

    if s not in _dict:
        compressed.append(count)
    else:
        compressed.append(_dict[s])

    file = open(out,'w')
    s = ''
    for i in compressed:
        s+= str(i) +' '
    file.write(s)
    file.close()

    keys = []
    values = []
    for key in _dict:
        keys.append(_dict[key])
        values.append(key)
    dict_path = out[:-4]+'_dict.csv'
    encoded = {'keys': list(keys), 'values' :list(values) }
    df = pd.DataFrame(encoded)
    df.to_csv(dict_path,index = False)

def decode(inp, out):
    dict_path = inp[:-4]+'_dict.csv'

    # read compressed data
    data = []
    with open(inp) as f:
        content = f.readlines()
    for line in content:
        if line != '':
            data.extend(list(map(int,line.strip().split(' '))))

    # read dictionary
    df = pd.read_csv(dict_path)
    keys = list(map(int,df['keys']))
    values = list(df['values'])
    _dict = dict(zip(keys,values))

    #decode
    s = ''
    for sym in data:
        s+=_dict[sym]

    #save decoded data
    file = open(out,'w')
    file.write(s)
    file.close()


def lzw(name):
    data_path = 'Data/' + name + '.txt'
    encode_path = 'Compressed/' + name + '_LZW.txt'
    decode_path = 'Decompressed/' + name + '_LZW.txt'
    encode(data_path, encode_path)
    decode(encode_path, decode_path)