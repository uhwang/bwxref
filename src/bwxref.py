'''
    bwxref.py
    
    2/2/21  Ver 0.1
    2/4/21  Multiple Korean Bible DB
            Added BibleWorks Export 

'''
import re
import os
import sqlite3 as db
import xreflib
import xrefcom
import clipboard
import HTML 
 
write_format = ['Txt', 'Docx', 'Html']

# Isa 66:5 
# Eze 16:52-56

#_nkr_db_table_name = "Bible"
_xref_kbible_listfile = "kbible_list.txt"
#_find_bwverse = re.compile('(.*)(?<=\s)(\d*):(\d*[-\d*]*)')
#_find_bwverse = re.compile('(.*)(?<=\s)(\d*):(\d*[-\d*]*)([,\d*]*)')
_find_bwverse = re.compile('(.*)(?<=\s)(\d*):(\d*[-\d*]*)([,\s*\d*a-z]*)')
        
class xref_elem:
    def __init__(self, book=None, chap=None, v1=0, v2=0):
        self.book = book
        self.chap = chap
        self.v1   = v1
        self.v2   = v2
        self.vlist= []

xref_list = []
kbible_list = []
kbible_check_list = {}
    
def read_kbible_list(): 
    global kbible_list, kbible_check_list
    
    try:
        fr = open(_xref_kbible_listfile, 'rt')
    except:
        fo = open(_xref_kbible_listfile, 'wt')
        
        fo.write('%d\n'%len(xreflib.korean_bible_name))
        
        for kb in xreflib.korean_bible_name:
            fo.write('%s\n'%kb)
        fo.close()
        fr = open(_xref_kbible_listfile, 'rt')
    
    kbible_list = []
    kbible_check_list = {}
    
    nb = int(fr.readline())
    for i in range(nb):
        kbn = fr.readline().strip()
        kbible_list.append(kbn)
        kbible_check_list[kbn] = True if kbn == "개역개정" else False
    fr.close()
        
def get_kbible_list():
    return kbible_list
    
def get_kbible_check_list():
    return kbible_check_list
    
def xref_to_txt(path, file, xref, db_list, msg):
    
    file = '%s.txt'%file
    msg.appendPlainText('... XRef to Txt\n... Open %s'%file)
    try:
        fo = open(os.path.join(path, file), 'wt')
    except Exception as e:
        e_str = str(e)
        msg.appendPlainText('... Error ==> %s'%e_str)
        xrefcom.message_box(xrefcom.message_error, e_str)
        return
    
    for x in xref:
        e = xreflib.table["%02d"%x.book]
        for key in db_list.keys():
            db_file = db_list[key]
            try:
                msg.appendPlainText('... Open DB %s'%db_file)
                db_con = db.connect(db_file)
                db_cur = db_con.cursor()
                table  = db_cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                db_tbl = table[0][0]
                fo.write('====== %s ======\n'%key)
            except Exception as e:
                e_str = str(e)
                msg.appendPlainText('... Error => %s'%e_str)
                xrefcom.message_box(xrefcom.message_error, e_str)
                return
            
            if x.v2 is 0:
                sql = 'SELECT btext from %s where book=%d '\
                      'and chapter=%d and verse=%d'%\
                      (db_tbl, x.book, x.chap, x.v1)
                      
                fo.write('%s %d:%d\n'%(e[2], x.chap, x.v1))
                
                for vtext in db_cur.execute(sql):
                    fo.write('%d. %s\n'%(x.v1, vtext[0]))
            else:
                sql = 'SELECT btext from %s where book=%d '\
                      'and chapter=%d and verse between %d and %d'%\
                      (db_tbl, x.book, x.chap, x.v1, x.v2)
                      
                fo.write('%s %d:%d-%d\n'%(e[2], x.chap, x.v1, x.v2))
                
                for i, vtext in enumerate(db_cur.execute(sql)):
                    fo.write('%d. %s\n'%(x.v1+i, vtext[0]))
        fo.write('\n')
        db_con.close()
        msg.appendPlainText('... Close DB')
    fo.write('\n')
    msg.appendPlainText('... Success')
    xrefcom.message_box(xrefcom.message_normal, 'Success')

def xref_to_docx(path, file, xref, db_list, msg):
    from docx import Document
    from docx.shared import Inches

    file = '%s.docx'%file
    msg.appendPlainText('... XRef to Docx\n... Open: %s'%file)

    ndb = len(db_list)
    document = Document()
    rows = len(xref)+1
    cols = ndb+1
    msg.appendPlainText('... Table(row,col): %d x %d'%(rows,cols))
    table = document.add_table(rows=rows, cols=cols)

    #for irow in range(rows): 
    #    table.add_row()
    
    table.rows[0].cells[0].text = "성경구절"
    
    for icol, (key, db_file) in enumerate(db_list.items()):
        icol += 1
        try:
            msg.appendPlainText('... Open DB %s'%db_file)
            db_con = db.connect(db_file)
            db_cur = db_con.cursor()
            db_tbls= db_cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            db_tbl = db_tbls[0][0]
        except Exception as e:
            e_str = str(e)
            #print('Error =>', str(e))
            msg.appendPlainText('... Error => %s'%e_str)
            xrefcom.message_box(xrefcom.message_error, e_str)
            return
        
        table.rows[0].cells[icol].text = key
            
        for irow, x in enumerate(xref):
            irow += 1
            #table.rows[irow].cells[0]._tc.tcPr.tcW.type = 'auto'
            #table.rows[irow].cells[0]._tc.tcPr.tcW.w = 0
        
            e = xreflib.table["%02d"%x.book]
                
            if x.v2 is 0:
                table.rows[irow].cells[0].text = '%s %d:%d'%(e[2], x.chap, x.v1)
                sql = 'SELECT btext from %s where book=%d '\
                    'and chapter=%d and verse=%d'%\
                    (db_tbl, x.book, x.chap, x.v1)
            
                for vtext in db_cur.execute(sql):
                    table.rows[irow].cells[icol].text = '%d. %s'%(x.v1, vtext[0])
            else:
                table.rows[irow].cells[0].text = '%s %d:%d-%d'%(e[2], x.chap, x.v1, x.v2)
                sql = 'SELECT btext from %s where book=%d '\
                      'and chapter=%d and verse between %d and %d'%\
                      (db_tbl, x.book, x.chap, x.v1, x.v2)
                vl = []
                for i, vtext in enumerate(db_cur.execute(sql)):
                    vl.append('%d. %s'%(x.v1+i, vtext[0]))
                table.rows[irow].cells[icol].text = '\n'.join(vl)
    
    try:
        document.save(os.path.join(path,file))
    except Exception as e:
        e_str = str(e)
        msg.appendPlainText('... Error ==> %s'%e_str)
        xrefcom.message_box(xrefcom.message_error, e_str)
        return
        
    msg.appendPlainText('... success')
    xrefcom.message_box(xrefcom.message_normal, 'Success')
            
def xref_to_html(path, file, xref, db_list, msg):
    file = '%s.html'%file
    msg.appendPlainText('... XRef to Html\n...Open %s'%file)
    try:
        fo = open(os.path.join(path, file), 'wt')
    except Exception as e:
        e_str = str(e)
        msg.appendPlainText('... Error ==> %s'%e_str)
        xrefcom.message_box(xrefcom.message_error, e_str)
        return
    
    head = [key for key in db_list.keys()]
    head.insert(0, ' ')
    html_table = HTML.Table(header_row=head)
    
    for x in xref:
        e = xreflib.table["%02d"%x.book]
        if x.v2 is 0:
            html_row = ['%s %d:%d'%(e[2], x.chap, x.v1)]
        else:
            html_row = ['%s %d:%d-%d\n'%(e[2], x.chap, x.v1, x.v2)]

        for col, (key, db_file) in enumerate(db_list.items()):
            db_file = db_list[key]
            try:
                msg.appendPlainText('... Open DB %s'%db_file)
                db_con = db.connect(db_file)
                db_cur = db_con.cursor()
                table  = db_cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                db_tbl = table[0][0]
            except Exception as e:
                e_str = str(e)
                msg.appendPlainText('... Error => %s'%e_str)
                xrefcom.message_box(xrefcom.message_error, e_str)
                return
            
            if x.v2 is 0:
                sql = 'SELECT btext from %s where book=%d '\
                      'and chapter=%d and verse=%d'%\
                      (db_tbl, x.book, x.chap, x.v1)
                      
                for vtext in db_cur.execute(sql):
                    html_row.append('%d. %s'%(x.v1, vtext[0]))
            else:
                sql = 'SELECT btext from %s where book=%d '\
                      'and chapter=%d and verse between %d and %d'%\
                      (db_tbl, x.book, x.chap, x.v1, x.v2)
                      
                vl = []
                for i, vtext in enumerate(db_cur.execute(sql)):
                    vl.append('<p>%d. %s</p>'%(x.v1+i, vtext[0]))
                html_row.append(''.join(vl))
        html_table.rows.append(html_row)
        db_con.close()
        msg.appendPlainText('... Close DB')
    fo.write(str(html_table))
    msg.appendPlainText('... Success')
    xrefcom.message_box(xrefcom.message_normal, 'Success')
    
write_xref = { 
    write_format[0] : xref_to_txt,  
    write_format[1] : xref_to_docx,  
    write_format[2] : xref_to_html,  
}

def get_write_format_txt():
    return write_format[0]
    
def get_write_format_docx():
    return write_format[1]

def get_write_format_html():
    return write_format[2]
    
def xref_to_kor(path, file, type, fmt=write_format[0], db_list=None, msg=None):
    global xref_list
   
    msg.appendPlainText('... xref_to_kor\n... Get clipboard data')
    try:
       verselist = clipboard.paste().split('\n')
    except Exception as e:
        #print('Error =>', str(e))
        e_str = str(e)
        msg.appendPlainText('... Error => %s'%e_str)
        xrefcom.message_box(xrefcom.message_error, e_str)
        return
    
    if not verselist: 
        e_str = 'Error => No clipboard data!'
        msg.appendPlainText('... %s'%e_str)
        xrefcom.message_box(xrefcom.message_warning, e_str)
        return
    
    xref_list = []
    abnormal_book = False
    
    for v in verselist:
        match = _find_bwverse.search(v)
        if match:
            #print(match.group(0))
            book = match.group(1).strip()
            num  = xreflib.get_book_num(book, type)
            if num < 0:
                msg.appendPlainText('... Non-canon book: %s'%book)
                abnormal_book = True
                continue
                
            ngroup= len(match.groups())
            book  = int(num)
            chap  = int(match.group(2))
            verse = match.group(3)
            extra = match.group(4)

            if verse.find('-') > -1:
                vv = verse.split('-')
                v1 = int(vv[0])
                v2 = int(vv[1])
                xref = xref_elem(book, chap, v1, v2)
            elif extra.find(',') > -1:
                # example: Matt. 24:3,27,37,39
                xref_list.append(xref_elem(book, chap, int(verse)))
                vv = extra.split(',')
                vv.pop(0)
                for v1 in vv:
                    v2 = re.sub('[a-z]*', '', v1.strip())
                    xref_list.append(xref_elem(book, chap, int(v2)))
                continue
            else:
                xref = xref_elem(book, chap, int(verse))
                
            xref_list.append(xref)

    if len(xref_list) is 0:
        e_str = 'Error => No verse exist! Check Clipboard!'
        msg.appendPlainText('... %s'%e_str)
        xrefcom.message_box(xrefcom.message_warning, e_str)
        return
        
    write_xref[fmt](path, file, xref_list, db_list, msg)
    if abnormal_book: 
        xrefcom.message_box(xrefcom.message_normal, "Check the message")
    msg.appendPlainText('... Success')
    
#xref_to_kor("xref.docx", write_format[1])
#xref_to_kor("xref.txt", write_format[0])
