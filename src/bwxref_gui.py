'''
    bwxref-gui.py
    
    2/3/21  Ver 0.1
    2/4/21  Added BibleWorks Export 
    2/11/21 WTT Mapping
    mportError: (cannot import name _elementpath) 'C:\\Users\\ul20a\\OneDrive - Southwestern Baptist Theological Seminary\\Python\\bwxref\\XRef\\lxml.etree.pyd'
Traceback (most recent call last):

    English Bible
    
    ESV    : English Standard Version
    GNT    : Good News Translation
    HCSB   : Holman Christian Standard bible
    ISV    : International Standard Version
    KJV    : King James Version
    MSG    : Message Version
    NAS1995: New American Standard Version
    NIV1984: New Internation Version (as literal as possible)
             NIV 2011 adopted neuteral vocabularies and changed grammatical
             inconsistency such as the mismatch of a subject(sing/plr) and verb
    NKJV   : New King James Version
    NLT    : New Living Translation
    NRSV   : New Revised Standard Version (liberal)
    YLT    : Young's Literal Translation
    
'''

import os
import sys
from PyQt4 import QtCore, QtGui
from collections import OrderedDict 

import bwxreflib
import bwxref
import bwxrefwtt

import icon_bwxref
import icon_docx
import icon_html
import icon_txt
import icon_folder_open
import icon_copy_src_path
import icon_save
import icon_load
import icon_trash

_xref_tab_text      = 'XRef'
_kdb_tab_text       = 'KDB'
_edb_tab_text       = 'EDB'
_check_db_tab_text  = 'Check'
_message_tab_text   = 'Message'
_kbible_path_file   = 'kbible_path.txt'
_ebible_path_file   = 'ebible_path.txt'
_default_output_file= 'xref'
_change_path_key    = ['Current', "All"]
_korean_bible_key   = 'kor'
_english_bible_key  = 'eng'

class QKeyButton(QtGui.QPushButton):
    def __init__(self, key):
        super(QKeyButton, self).__init__()
        self.key = key
        
class QChangePath(QtGui.QDialog):
    # db is Tab label ('KDB' or 'EDB')
    def __init__(self, bwx, db_key):
        super(QChangePath, self).__init__()
        self.bwx = bwx
        self.db_key = db_key
        self.initUI()
        
    def initUI(self):
        layout = QtGui.QFormLayout()
        # Create an array of radio buttons
        self.moods = [QtGui.QRadioButton(_change_path_key[0]), 
                      QtGui.QRadioButton(_change_path_key[1])]

        # Radio buttons usually are in a vertical layout   
        source_layout = QtGui.QHBoxLayout()

        # Create a button group for radio buttons
        self.mood_button_group = QtGui.QButtonGroup()

        for i in range(len(self.moods)):
            # Add each radio button to the button layout
            source_layout.addWidget(self.moods[i])
            # Add each radio button to the button group & give it an ID of i
            self.mood_button_group.addButton(self.moods[i], i)
            # Connect each radio button to a method to run when it's clicked
            self.connect(self.moods[i], QtCore.SIGNAL("clicked()"), self.radio_button_clicked)

        # Set a radio button to be checked by default
        self.moods[0].setChecked(True)   
        
        source_type_layout = QtGui.QVBoxLayout()
        self.bible_list = QtGui.QComboBox()
        if self.db_key == _kdb_tab_text:
            self.bible_list.addItems(self.bwx.get_kdb_path())
        else:
            self.bible_list.addItems(self.bwx.get_edb_path())
            
        source_type_layout.addWidget(self.bible_list)
        
        button_layout = QtGui.QHBoxLayout()
        self.ok = QtGui.QPushButton('OK')
        self.ok.clicked.connect(self.accept)
        button_layout.addWidget(self.ok)

        self.no = QtGui.QPushButton('Cancel')
        self.no.clicked.connect(self.reject)
        button_layout.addWidget(self.no)

        layout.addRow(source_layout)
        layout.addRow(source_type_layout)
        layout.addRow(button_layout)
        self.setLayout(layout)
        self.setWindowTitle('Change Path')
        self.radio_button_clicked()
        
    def radio_button_clicked(self):
        self.id = self.mood_button_group.checkedId()
        #if id == 0: # get output name from ppt files
        #    self.ppt_list.setEnabled(True)
        #    self.user_input.setEnabled(False)
        #elif id == 1: # get output name from user input
        #    self.ppt_list.setEnabled(False)
        #    self.user_input.setEnabled(True)
    
    def get_source(self):
        return self.moods[self.mood_button_group.checkedId()].text(), self.bible_list.currentText()


class XRefConvert(QtGui.QWidget):
    def __init__(self):
        super(XRefConvert, self).__init__()
        self.initUI()
        
    def initUI(self):
        bwxref.read_kbible_list()
        bwxref.read_ebible_list()

        form_layout = QtGui.QFormLayout()
        tab_layout  = QtGui.QVBoxLayout()
        self.tabs   = QtGui.QTabWidget()
        policy      = self.tabs.sizePolicy()
        policy.setVerticalStretch(1)
        self.tabs.setSizePolicy(policy)
        self.tabs.setEnabled(True)
        self.tabs.setTabPosition(QtGui.QTabWidget.West)
        
        self.xref_tab    = QtGui.QWidget()
        self.kdb_tab     = QtGui.QWidget()
        self.edb_tab     = QtGui.QWidget()
        self.check_db_tab= QtGui.QWidget()
        self.message_tab = QtGui.QWidget()
        
        self.tabs.addTab(self.xref_tab    , _xref_tab_text)
        self.tabs.addTab(self.kdb_tab      , _kdb_tab_text)
        self.tabs.addTab(self.edb_tab      , _edb_tab_text)
        self.tabs.addTab(self.check_db_tab, _check_db_tab_text)
        self.tabs.addTab(self.message_tab , _message_tab_text)
        
        self.message_tab_UI()
        self.xref_tab_UI()
        self.db_tab_UI('kor')
        self.db_tab_UI('eng')
        self.check_db_tab_UI()

        tab_layout.addWidget(self.tabs)
        form_layout.addRow(tab_layout)
        self.setLayout(form_layout)
        
        self.setWindowTitle("XRef")
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(icon_bwxref.table)))
        self.show()
        
    def get_kdb_path(self):
        return [self.kbible_path[key].text() for key in self.kbible_path.keys()]
        
    def get_edb_path(self):
        return [self.ebible_path[key].text() for key in self.ebible_path.keys()]
    
    def xref_tab_UI(self):
        form_layout  = QtGui.QFormLayout()
        layout = QtGui.QGridLayout()
        
        layout.addWidget(QtGui.QLabel("Name"), 0,0)
        self.xref_output = QtGui.QLineEdit(_default_output_file)
        layout.addWidget(self.xref_output, 0, 1)
        
        layout.addWidget(QtGui.QLabel("Path"), 1,0)
        self.xref_output_path = QtGui.QLineEdit(os.getcwd())
        layout.addWidget(self.xref_output_path, 1, 1)
        self.xref_output_path_btn = QtGui.QPushButton()
        self.xref_output_path_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_folder_open.table)))
        self.xref_output_path_btn.setIconSize(QtCore.QSize(24,24))
        self.connect(self.xref_output_path_btn, QtCore.SIGNAL('clicked()'), self.choose_output_folder)

        layout.addWidget(self.xref_output_path_btn, 1, 2)
        form_layout.addRow(layout)

        layout = QtGui.QGridLayout()
        layout.addWidget(QtGui.QLabel("Clipboard Data type"), 0, 0)
        self.xref_type_combo = QtGui.QComboBox()
        self.xref_type_combo.addItems(bwxreflib.xref_type)
        self.xref_type_combo.currentIndexChanged.connect(self.set_wtt_mapping)
        
        layout.addWidget(self.xref_type_combo, 0, 1)
        layout.addWidget(QtGui.QLabel("WTT Mapping"), 1, 0)
        self.wtt_mapping_chk = QtGui.QCheckBox()
        self.wtt_mapping_chk.setChecked(False)
        self.wtt_mapping_chk.stateChanged.connect(self.enable_wtt_map_key)
        layout.addWidget(self.wtt_mapping_chk, 1, 1)
        
        layout.addWidget(QtGui.QLabel("Map Version"), 2, 0)
        self.wtt_map_key_cmb = QtGui.QComboBox()
        self.wtt_map_key_cmb.addItems(bwxrefwtt.wtt_map_key)
        self.wtt_map_key_cmb.setEnabled(False)
        layout.addWidget(self.wtt_map_key_cmb, 2,1)
        
        form_layout.addRow(layout)
  
        layout = QtGui.QHBoxLayout()
        self.xref_save_txt_btn = QKeyButton(bwxref.get_write_format_txt())       
        self.xref_save_txt_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_txt.table)))
        self.xref_save_txt_btn.setIconSize(QtCore.QSize(24,24))
        self.xref_save_txt_btn.setText(bwxref.get_write_format_txt())
        self.connect(self.xref_save_txt_btn, QtCore.SIGNAL('clicked()'), self.save_xref)

        self.xref_save_docx_btn = QKeyButton(bwxref.get_write_format_docx())       
        self.xref_save_docx_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_docx.table)))
        self.xref_save_docx_btn.setIconSize(QtCore.QSize(24,24))
        self.xref_save_docx_btn.setText(bwxref.get_write_format_docx())
        self.connect(self.xref_save_docx_btn, QtCore.SIGNAL('clicked()'), self.save_xref)

        self.xref_save_html_btn = QKeyButton(bwxref.get_write_format_html())
        self.xref_save_html_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_html.table)))
        self.xref_save_html_btn.setIconSize(QtCore.QSize(24,24))
        self.xref_save_html_btn.setText(bwxref.get_write_format_html())
        self.connect(self.xref_save_html_btn, QtCore.SIGNAL('clicked()'), self.save_xref)
        
        layout.addWidget(self.xref_save_txt_btn)
        layout.addWidget(self.xref_save_docx_btn)
        layout.addWidget(self.xref_save_html_btn)
        
        form_layout.addRow(layout)
        
        self.xref_tab.setLayout(form_layout)
    
    def enable_wtt_map_key(self):
        if self.wtt_mapping_chk.isChecked():
            self.wtt_map_key_cmb.setEnabled(True)
        else:
            self.wtt_map_key_cmb.setEnabled(False)
            
    def set_wtt_mapping(self):
        if self.xref_type_combo.currentText() == bwxreflib.get_xref_type_bwxref():
            self.wtt_mapping_chk.setChecked(False)
        else:
            self.wtt_mapping_chk.setChecked(True)
            
    def db_tab_UI(self, key):
        form_layout  = QtGui.QFormLayout()
        layout = QtGui.QHBoxLayout()
        
        copy_btn = QtGui.QPushButton()
        copy_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_copy_src_path.table)))
        copy_btn.setIconSize(QtCore.QSize(16,16))
        self.connect(copy_btn, QtCore.SIGNAL('clicked()'), self.apply_source_path_all)
       
        save_btn = QtGui.QPushButton()
        save_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_save.table)))
        save_btn.setIconSize(QtCore.QSize(16,16))

        load_btn = QtGui.QPushButton()
        load_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_load.table)))
        load_btn.setIconSize(QtCore.QSize(16,16))

        if key == _korean_bible_key:
            self.copy_kbible_path_btn = copy_btn
            self.save_kbible_path_btn = save_btn
            self.load_kbible_path_btn = load_btn
            self.connect(self.save_kbible_path_btn, QtCore.SIGNAL('clicked()'), self.save_bible_path)
            self.connect(self.load_kbible_path_btn, QtCore.SIGNAL('clicked()'), self.load_kbible_path)
        elif key == _english_bible_key:
            self.copy_ebible_path_btn = copy_btn
            self.save_ebible_path_btn = save_btn
            self.load_ebible_path_btn = load_btn
            self.connect(self.save_ebible_path_btn, QtCore.SIGNAL('clicked()'), self.save_bible_path)
            self.connect(self.load_ebible_path_btn, QtCore.SIGNAL('clicked()'), self.load_ebible_path)
        
        layout.addWidget(copy_btn)
        layout.addWidget(save_btn)
        layout.addWidget(load_btn)
        form_layout.addRow(layout)
        
        grid = QtGui.QGridLayout()
        grid.addWidget(QtGui.QLabel("Bible" ), 0,0)
        grid.addWidget(QtGui.QLabel("DB"    ), 0,1)
        grid.addWidget(QtGui.QLabel("Path"  ), 0,2)
        grid.addWidget(QtGui.QLabel("Folder"), 0,3)
        
        if key == _korean_bible_key:
            self.kbible_layout = grid
            self.kbible_file = {}
            self.kbible_path = {}
            self.kbible_select= {}
            
            bbl = bwxref.get_kbible_list()
            file = self.kbible_file
            path = self.kbible_path
            select = self.kbible_select
        elif key == _english_bible_key:
            self.ebible_layout = grid
            self.ebible_file = {}
            self.ebible_path = {}
            self.ebible_select= {}

            bbl = bwxref.get_ebible_list()
            file = self.ebible_file
            path = self.ebible_path
            select = self.ebible_select

        for i, bn in enumerate(bbl):
            file  [bn] = QtGui.QLineEdit()
            path  [bn] = QtGui.QLineEdit()
            select[bn] = QKeyButton(bn)
            select[bn].setIcon(QtGui.QIcon(QtGui.QPixmap(icon_folder_open.table)))
            select[bn].setIconSize(QtCore.QSize(16,16))
            self.connect(select[bn], QtCore.SIGNAL('clicked()'), self.select_source_path)
            
            ii = i+1
            grid.addWidget(QtGui.QLabel(bn)      , ii,0)
            grid.addWidget(file[bn]  , ii,1)
            grid.addWidget(path[bn]  , ii,2)
            grid.addWidget(select[bn], ii,3)
          
        # minimize vertical spacing
        grid.setContentsMargins(0,0,0,0)
        grid.setSpacing(0)
        
        #form_layout.addRow(self.kbible_layout)
        form_layout.addRow(grid)
        if key == _korean_bible_key: 
            self.kdb_tab.setLayout(form_layout)
            # load db info
            self.load_kbible_path()
        if key == _english_bible_key: 
            self.edb_tab.setLayout(form_layout)
            # load db info
            self.load_ebible_path()
        
    def check_db_tab_UI(self):
        layout = QtGui.QFormLayout()

        kbib_group = QtGui.QGroupBox('Korean Bible')
        kbib_layout = QtGui.QGridLayout()
        kcheck_list = bwxref.get_kbible_check_list()
        self.kbible_checker = {}
        ncol = 3
        row = 0

        for i, kbib in enumerate(bwxref.get_kbible_list()):
            checker = QtGui.QCheckBox(kbib, self)
            checker.setChecked(kcheck_list[kbib])
            self.kbible_checker[kbib] = checker
            col = i % ncol
            row = row+1 if i is not 0 and i%ncol is 0 else row
            kbib_layout.addWidget(self.kbible_checker[kbib], row, col)
            
        kbib_group.setLayout(kbib_layout)
        layout.addRow(kbib_group)		
        
        ebib_group = QtGui.QGroupBox('English Bible')
        ebib_layout = QtGui.QGridLayout()
        echeck_list = bwxref.get_ebible_check_list()
        self.ebible_checker = {}
        ncol = 3
        row = 0

        for i, ebib in enumerate(bwxref.get_ebible_list()):
            checker = QtGui.QCheckBox(ebib, self)
            checker.setChecked(echeck_list[ebib])
            self.ebible_checker[ebib] = checker
            col = i % ncol
            row = row+1 if i is not 0 and i%ncol is 0 else row
            ebib_layout.addWidget(self.ebible_checker[ebib], row, col)
            
        ebib_group.setLayout(ebib_layout)
        layout.addRow(ebib_group)		
        
        
        hgbib_group = QtGui.QGroupBox('Hebrew/Greek Bible')
        hgbib_layout = QtGui.QGridLayout()
        hgcheck_list = bwxref.get_hgbible_check_list()
        self.hgbible_checker = {}
        ncol = 3
        row = 0
        for i, hgbib in enumerate(bwxref.get_hgbible_list()):
            checker = QtGui.QCheckBox(hgbib, self)
            checker.setChecked(hgcheck_list[hgbib])
            self.hgbible_checker[hgbib] = checker
            checker.setEnabled(False)
            col = i % ncol
            row = row+1 if i is not 0 and i%ncol is 0 else row
            hgbib_layout.addWidget(self.hgbible_checker[hgbib], row, col)
        hgbib_group.setLayout(hgbib_layout)  
        layout.addRow(hgbib_group)	
        
        self.check_db_tab.setLayout(layout)
    
    def delete_message(self):
        self.message.clear()
        
    def message_tab_UI(self):
        form_layout  = QtGui.QFormLayout()
        
        layout = QtGui.QHBoxLayout()
        self.delete_message_btn = QtGui.QPushButton('Clear')
        #self.delete_message_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_trash.table)))
        #self.delete_message_btn.setIconSize(QtCore.QSize(24,24))
        self.connect(self.delete_message_btn, QtCore.SIGNAL('clicked()'), self.delete_message)
        layout.addWidget(self.delete_message_btn)
       
        form_layout.addRow(layout)
        
        self.message = QtGui.QPlainTextEdit()
		# Plain Editor resize
        policy = self.sizePolicy()
        policy.setVerticalStretch(1)
        self.message.setSizePolicy(policy)
        form_layout.addRow(self.message)
        self.message_tab.setLayout(form_layout)
        
    def select_source_path(self):
        btn = self.sender()
        file = QtGui.QFileDialog.getOpenFileName(self, "%s DB"%btn.key, directory=os.getcwd())
        if not file: return
        fpath, fname = os.path.split(file)
        
        tab_name = self.tabs.tabText(self.tabs.currentIndex())
        if tab_name == _kdb_tab_text:
            self.kbible_file  [btn.key].setText(fname)
            self.kbible_path  [btn.key].setText(fpath)
        elif tab_name == _edb_tab_text:            
            self.ebible_file  [btn.key].setText(fname)
            self.ebible_path  [btn.key].setText(fpath)
       
    # 개역개정,d:\한글DB,개역개정.bdb
    # 개역한글,d:\한글DB,개역한글.bdb
    # 개역개정-국한문,d:\한글DB,개정국한문.bdb
    # 공동번역개정,d:\한글DB,공동번역.bdb
    # 바른성경,d:\한글DB,바른성경.bdb
    # 새번역,d:\한글DB,새번역.bdb
    # 쉬운성경,d:\한글DB,쉬운성경.bdb
    # 우리말성경,d:\한글DB,우리말.bdb
    # 카톨릭성경,d:\한글DB,카톨릭.bdb 
    # 킹제임스흠정역,d:\한글DB,킹흠정역.bdb
    # 한글킹제임스,d:\한글DB,한글킹.bdb 
    # 현대어성경,d:\한글DB,현대어.bdb
    # 현대인성경,d:\한글DB,현대인.bdb
    def save_bible_path(self):#, key, path_file):
        
        if self.bible_path_key == _korean_bible_key:
            file = self.kbible_file
            path = self.kbible_path
            path_file = _kbible_path_file
        elif self.bible_path_key == _english_bible_key:
            file = self.ebible_file
            path = self.ebible_path
            path_file = _ebible_path_file
            
        try:
            self.message.appendPlainText('... Save %s Bible'%self.bible_path_key)
            with open(path_file, "wt") as fo:
                #keys = file.keys()
                nb = len(file)
                self.message.appendPlainText('... %d files'%nb)
                fo.write('%d\n'%nb)
                for key in file.keys():
                    ff = file[key]
                    fp = path[key]
                    fo.write("%s,%s,%s\n" %(key, fp.text(), ff.text()))
        except Exception as e:
            self.message.appendPlainText('... Error(save_bible_path) ==> %s'%str(e))
            return
        self.message.appendPlainText('... Success')
     
    def load_kbible_path(self):
        self.bible_path_key = _korean_bible_key
        self.load_bible_path()
        
    def load_ebible_path(self):
        self.bible_path_key = _english_bible_key
        self.load_bible_path()
        
    def load_bible_path(self):#, key, path_file):
        if self.bible_path_key == _korean_bible_key:
            file = self.kbible_file
            path = self.kbible_path
            path_file = _kbible_path_file
        elif self.bible_path_key == _english_bible_key:
            file = self.ebible_file
            path = self.ebible_path
            path_file = _ebible_path_file
        try:
            self.message.appendPlainText('... Load %s Bible'%self.bible_path_key)
            with open(path_file, "rt") as fr:
                nb = fr.readline()
                self.message.appendPlainText('... Read %d files'%int(nb))
                for line in fr:
                    info = line.strip().split(',')
                    bn = info[0].strip()
                    path[bn].setText(info[1].strip())
                    file[bn].setText(info[2].strip())
        except Exception as e:
            self.message.appendPlainText('... Error(load_bible_path) ==> %s'%str(e))   
            return
            
        self.message.appendPlainText('... Success')   
        
    def apply_source_path_all(self):
        tab_text = self.tabs.tabText(self.tabs.currentIndex())
        change_path_dlg = QChangePath(self, tab_text)
		
        if change_path_dlg.exec_() is not 1:
            return
            
        type, src_path = change_path_dlg.get_source()
        
        if type == _change_path_key[0]: #current
            if tab_text == _kdb_tab_text:
                dest_path = self.kbible_path
            else:
                dest_path = self.ebible_path
            
            for k in dest_path.keys():
                dest_path[k].setText(src_path) 
        else: #all
            dest_path = [self.kbible_path, self.ebible_path]
            for path in dest_path:
                for k in path.keys():
                    path[k].setText(src_path) 
        
    def choose_output_folder(self):
        cur_path = os.getcwd() 
        path = QtGui.QFileDialog.getExistingDirectory(None, 'Save folder', cur_path, 
        QtGui.QFileDialog.ShowDirsOnly)
        if not path: return
        self.xref_output_path.setText(path)
        
    def confirm_db_check(self):
        kcheck_list = bwxref.get_kbible_check_list()
        echeck_list = bwxref.get_ebible_check_list()
        self.db_list = {}

        for key, checker in self.kbible_checker.items():
            kcheck_list[key] = checker.isChecked()
            if kcheck_list[key] is True:
                self.db_list[key] = os.path.join(self.kbible_path[key].text(), 
                                                self.kbible_file[key].text())
    
        for key, checker in self.ebible_checker.items():
            echeck_list[key] = checker.isChecked()
            if echeck_list[key] is True:
                self.db_list[key] = os.path.join(self.ebible_path[key].text(), 
                                                self.ebible_file[key].text())
        
    def get_output_file(self):
        return os.path.join(self.xref_output_path.text(), self.xref_output.text())
        
    def get_map_table(self):
        map_key = self.wtt_map_key_cmb.currentText()
        return (map_key, bwxrefwtt.get_wtt_map_version(map_key))\
               if self.wtt_mapping_chk.isChecked() else (map_key, None)
        
        
    def save_xref(self):
        btn = self.sender()
        self.message.appendPlainText('... xref to %s'%btn.key)
        self.confirm_db_check()
        path, file = self.xref_output_path.text(), self.xref_output.text()
        bwxref.xref_to_kor(path, 
                           file, 
                           self.xref_type_combo.currentText(),
                           btn.key,
                           self.wtt_mapping_chk.isChecked(),
                           self.get_map_table(),                       
                           self.db_list, 
                           self.message)

def main(): 
    app = QtGui.QApplication(sys.argv)
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'Plastique'))
    run = XRefConvert()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
