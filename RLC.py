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
        if curr_sym != c:
            sym.append(c)
            fre.append(1)
            curr_sym = c
        else:
            fre[-1]+=1

    #save data compressed
    compressed = {'symbol' : sym, 'frequency': fre}
    df = pd.DataFrame(compressed)
    df.to_csv(out,index = False)


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

def rlc(name):
    data_path = 'Data/'+name+'.txt'
    encode_path = 'Compressed/'+name+'_RLC.txt'
    decode_path = 'Decompressed/'+name+'_RLC.txt'
    encode(data_path,encode_path)
    decode(encode_path,decode_path)
