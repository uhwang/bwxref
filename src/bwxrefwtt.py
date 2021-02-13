# bwxrefwtt.py
# 2/11/21

import re
import bwxreflib

import wtt_map_nau
import wtt_map_bgm
import wtt_map_bgt
import wtt_map_wtt

wtt_map_languages = ['English', 'Greek', 'Hebrew']

wtt_map_key = ['NAU', 'BGM', 'BGT', 'WTT']

def get_wtt_map_key_nau(): return wtt_map_key[0]
def get_wtt_map_key_bgm(): return wtt_map_key[1]
def get_wtt_map_key_bgt(): return wtt_map_key[2]
def get_wtt_map_key_wtt(): return wtt_map_key[3]

wtt_map_version = {
    wtt_map_key[0] : wtt_map_nau.table,
    wtt_map_key[1] : wtt_map_bgm.table,
    wtt_map_key[2] : wtt_map_bgt.table,
    wtt_map_key[3] : wtt_map_wtt.table
} 

def get_wtt_map_version(key):
    return wtt_map_version[key]

# file : ???.vfm

#Gen 31:55 Gen 32:1 WTT
#Gen 32:1-32 Gen 32:2-33 WTT

def get_chap_verse(e):
    e1 = e.split(':')
    if e1[1].find('-') > 0:
        e2 = e1[1].split('-')
        v1 = int(e2[0])
        v2 = int(e2[1])
    else:
        v1 = int(e1[1])
        v2 = 0
    return int(e1[0]), v1, v2
        
def create_wtt_map(key, file):
    wtt_key = get_wtt_map_key_wtt()
    try:
        map_file = "wtt_map_%s.py"%key.lower()
        fr = open(file, 'rt')
        fo = open(map_file, 'wt')
        
        fo.write('table = {\n')
        
        for line in fr:
            g = line.split(' ')
            book_src = bwxreflib.get_book_num(g[0], bwxreflib.get_xref_type_bwxref())
            if book_src < 0: 
                continue
            chap_src, v1_src, v2_src = get_chap_verse(g[1])
            chap_dest, v1_dest, v2_dest = get_chap_verse(g[3])
            
            if v2_src > 0:
                vs = [v for v in range(v1_src, v2_src+1)]
                vd = [v for v in range(v1_dest, v2_dest+1)]

                for vs1, vd1 in zip(vs, vd):
                    if key == wtt_key:
                        fo.write("\'%02d:%d:%d\': (%d,%d),\n"%(
                        book_src, chap_dest, vd1, 
                                  chap_src , vs1))
                    else:
                        fo.write("\'%02d:%d:%d\': (%d,%d),\n"%(
                        book_src, chap_src , vs1, 
                                  chap_dest, vd1))
            else:
                if key == wtt_key:
                    fo.write("\'%02d:%d:%d\': (%d,%d),\n"%(\
                        book_src, chap_dest, v1_dest,
                                  chap_src , v1_src))
                else:
                    fo.write("\'%02d:%d:%d\': (%d,%d),\n"%(\
                        book_src, chap_src , v1_src,
                                  chap_dest, v1_dest))
                    
        fo.write('}')    
        fo.close()
        fr.close()
    except Exception as e:
        print('Error => %s'%str(e))
        
#create_wtt_map(wtt_map_key[0], 'nau.vmf')
#create_wtt_map(wtt_map_key[1], 'bgt.vmf')
#create_wtt_map(wtt_map_key[2], 'bgm.vmf')
#create_wtt_map(wtt_map_key[3], 'nau.vmf')
