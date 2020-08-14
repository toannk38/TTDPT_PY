import RLC
import LZW
import ShannonFano as SF
import HuffmanCoding as HC
import pandas as pd

def main():
    num_files = 1
    names = [str(i+1) for i in range(num_files)]
    _RLC =  RLC.rlc(names)
    _LZW =  LZW.lzw(names)
    _SF =  SF.sf(names)
    _HC = HC.hc(names)

    RLC_ratio = [round(x[0]/x[1],2) for x in _RLC]
    LZW_ratio = [round(x[0]/x[1],2) for x in _LZW]
    SF_ratio =  [round(x[0]/x[1],2) for x in _SF]
    HC_ratio =  [round(x[0]/x[1],2) for x in _HC]

    statistic = {'files':names, 'RLC':RLC_ratio, 'LZW':LZW_ratio,'SF':SF_ratio, 'HC':HC_ratio}

    df = pd.DataFrame(statistic)
    df.to_csv('statistic.csv',index= False)


main()

