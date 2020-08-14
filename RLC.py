import pandas as pd


def encode(inp,out):
    #read data
    with open(inp) as f:
        content = f.readlines()
    content = ''.join(content)

    if content == '':
        return

    #initial
    curr_sym = ''
    sym  = [] #symbol
    fre = [] #frequency'

    #compress data
    for c in content:
        if curr_sym != c or fre[-1] == 15:
            sym.append(c)
            fre.append(1)
            curr_sym = c
        else:
            fre[-1]+=1

    #save data compressed
    compressed = {'symbol' : sym, 'frequency': fre}
    df = pd.DataFrame(compressed)
    df.to_csv(out,index = False)

    '''
    data using 8 bits for every symbol
    encode using 8 bits for symbol and 4 bits for frequency (frequency <=15)
    '''
    bits_data = len(content*8)
    bits_compressed = len(fre)*12
    return bits_data, bits_compressed


def decode(inp,out):
    data = pd.read_csv(inp)
    sym = list(data['symbol'])
    fre = list(map(int,data['frequency']))

    s = ''
    for i in range(len(sym)):
        s += sym[i]*fre[i]

    file  = open(out,'w')
    file.write(s)
    file.close()


def rlc(names):
    for name in names:
        data_path = 'Data/'+name+'.txt'
        encode_path = 'Compressed/'+name+'_RLC.txt'
        decode_path = 'Decompressed/'+name+'_RLC.txt'
        bits = encode(data_path,encode_path)
        decode(encode_path,decode_path)
        return bits
