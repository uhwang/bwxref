'''
    bwxref-gui.py
    
    2/3/21  Ver 0.1
    2/4/21  Added BibleWorks Export 

'''
import xreflib
import bwxref
import os
import sys

#import tkinter as tk
#from tkinter import ttk
#
#window = tk.Tk()
#window.title('BW ref to kor')
#
#frame = tk.Frame
#
#main_tab    = ttk.Notebook(window)
#xref_tab    = ttk.Frame(main_tab)
#setting_tab = ttk.Frame(main_tab)
#
#main_tab.add(xref_tab   , text='XRef')
#main_tab.add(setting_tab, text='Setting')
#main_tab.pack(expand = 1, fill ="both") 
#
#n = tk.StringVar() 
#write_type = ttk.Combobox(xref_tab, width = 27, textvariable = n)
#write_type['values'] = [x for x in bwxref.write_format]
#write_type.grid(column = 1, row = 5) 
#write_type.current() 
#
#window.mainloop()

from PyQt4 import QtCore, QtGui

import bwxref

import icon_bwxref
import icon_docx
import icon_html
import icon_txt
import icon_folder_open
import icon_copy_src_path
import icon_save
import icon_load
import icon_trash

_xref_tab_text     = 'XRef'
_db_tab_text       = 'KDB'
_check_db_tab_text = 'KCheck'
_message_tab_text  = 'Message'
_kbible_path_file  = 'kbible_path.txt'
_default_output_file = 'xref'


class QBibleDatabaseButton(QtGui.QPushButton):
    def __init__(self, kbib):
        super(QBibleDatabaseButton, self).__init__()
        self.kbib = kbib
        
class XRefConvert(QtGui.QWidget):
    def __init__(self):
        super(XRefConvert, self).__init__()
        self.initUI()
        
    def initUI(self):
        bwxref.read_kbible_list()

        form_layout = QtGui.QFormLayout()
        tab_layout  = QtGui.QVBoxLayout()
        self.tabs   = QtGui.QTabWidget()
        policy      = self.tabs.sizePolicy()
        policy.setVerticalStretch(1)
        self.tabs.setSizePolicy(policy)
        self.tabs.setEnabled(True)
        self.tabs.setTabPosition(QtGui.QTabWidget.West)
        
        self.xref_tab    = QtGui.QWidget()
        self.db_tab      = QtGui.QWidget()
        self.check_db_tab= QtGui.QWidget()
        self.message_tab = QtGui.QWidget()
        
        self.tabs.addTab(self.xref_tab    , _xref_tab_text)
        self.tabs.addTab(self.db_tab      , _db_tab_text)
        self.tabs.addTab(self.check_db_tab, _check_db_tab_text)
        self.tabs.addTab(self.message_tab , _message_tab_text)
        
        self.message_tab_UI()
        self.xref_tab_UI()
        self.db_tab_UI()
        self.check_db_tab_UI()

        tab_layout.addWidget(self.tabs)
        form_layout.addRow(tab_layout)
        self.setLayout(form_layout)
        
        self.setWindowTitle("XRef")
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(icon_bwxref.table)))
        self.show()
        
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

        layout = QtGui.QHBoxLayout()
        layout.addWidget(QtGui.QLabel("Clipboard Data type"))
        self.xref_type_combo = QtGui.QComboBox()
        self.xref_type_combo.addItems(xreflib.xref_type)
        layout.addWidget(self.xref_type_combo)
        form_layout.addRow(layout)
  
        layout = QtGui.QHBoxLayout()
        self.xref_save_txt_btn = QtGui.QPushButton(bwxref.get_write_format_txt(), self)
        
        self.xref_save_txt_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_txt.table)))
        self.xref_save_txt_btn.setIconSize(QtCore.QSize(24,24))
        self.connect(self.xref_save_txt_btn, QtCore.SIGNAL('clicked()'), self.xref_save_txt)

        self.xref_save_docx_btn = QtGui.QPushButton(bwxref.get_write_format_docx(), self)
        
        self.xref_save_docx_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_docx.table)))
        self.xref_save_docx_btn.setIconSize(QtCore.QSize(24,24))
        self.connect(self.xref_save_docx_btn, QtCore.SIGNAL('clicked()'), self.xref_save_docx)

        self.xref_save_html_btn = QtGui.QPushButton(bwxref.get_write_format_html(), self)

        self.xref_save_html_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_html.table)))
        self.xref_save_html_btn.setIconSize(QtCore.QSize(24,24))
        self.connect(self.xref_save_html_btn, QtCore.SIGNAL('clicked()'), self.xref_save_html)
        
        layout.addWidget(self.xref_save_txt_btn)
        layout.addWidget(self.xref_save_docx_btn)
        layout.addWidget(self.xref_save_html_btn)
        
        form_layout.addRow(layout)
        
        self.xref_tab.setLayout(form_layout)
    
    def db_tab_UI(self):
        form_layout  = QtGui.QFormLayout()
        layout = QtGui.QHBoxLayout()
        
        self.copy_kbible_path_btn = QtGui.QPushButton()
        self.copy_kbible_path_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_copy_src_path.table)))
        self.copy_kbible_path_btn.setIconSize(QtCore.QSize(16,16))
        self.connect(self.xref_save_docx_btn, QtCore.SIGNAL('clicked()'), self.apply_source_path_all)
        
        self.save_kbible_path_btn = QtGui.QPushButton()
        self.save_kbible_path_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_save.table)))
        self.save_kbible_path_btn.setIconSize(QtCore.QSize(16,16))
        self.connect(self.save_kbible_path_btn, QtCore.SIGNAL('clicked()'), self.save_kbible_path)

        self.load_kbible_path_btn = QtGui.QPushButton()
        self.load_kbible_path_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_load.table)))
        self.load_kbible_path_btn.setIconSize(QtCore.QSize(16,16))
        self.connect(self.load_kbible_path_btn, QtCore.SIGNAL('clicked()'), self.load_kbible_path)
         
        layout.addWidget(self.copy_kbible_path_btn)
        layout.addWidget(self.save_kbible_path_btn)
        layout.addWidget(self.load_kbible_path_btn)
        form_layout.addRow(layout)
        
        self.kbible_layout = QtGui.QGridLayout()
        
        self.kbible_layout.addWidget(QtGui.QLabel("Bible" ), 0,0)
        self.kbible_layout.addWidget(QtGui.QLabel("DB"    ), 0,1)
        self.kbible_layout.addWidget(QtGui.QLabel("Path"  ), 0,2)
        self.kbible_layout.addWidget(QtGui.QLabel("Folder"), 0,3)
        
        self.kbible_file = {}
        self.kbible_path = {}
        self.kbible_select= {}
        kbl = bwxref.get_kbible_list()
        
        for i, bn in enumerate(kbl):
            self.kbible_file  [bn] = QtGui.QLineEdit()
            self.kbible_path  [bn] = QtGui.QLineEdit()
            self.kbible_select[bn] = QBibleDatabaseButton(bn)
            self.kbible_select[bn].setIcon(QtGui.QIcon(QtGui.QPixmap(icon_folder_open.table)))
            self.kbible_select[bn].setIconSize(QtCore.QSize(16,16))
            self.connect(self.kbible_select[bn], QtCore.SIGNAL('clicked()'), self.select_source_path)
            
            ii = i+1
            self.kbible_layout.addWidget(QtGui.QLabel(bn)      , ii,0)
            self.kbible_layout.addWidget(self.kbible_file[bn]  , ii,1)
            self.kbible_layout.addWidget(self.kbible_path[bn]  , ii,2)
            self.kbible_layout.addWidget(self.kbible_select[bn], ii,3)
            
        # minimize vertical spacing
        self.kbible_layout.setContentsMargins(0,0,0,0)
        self.kbible_layout.setSpacing(0)
        form_layout.addRow(self.kbible_layout)
        self.db_tab.setLayout(form_layout)

        # load db info
        self.load_kbible_path()
        
    def check_db_tab_UI(self):
        layout = QtGui.QFormLayout()
        kbib_group = QtGui.QGroupBox('Korean Bible')
        kbib_layout = QtGui.QGridLayout()

        check_list = bwxref.get_kbible_check_list()
        self.kbible_checker = {}
        ncol = 3
        row = 0

        for i, kbib in enumerate(bwxref.get_kbible_list()):
            checker = QtGui.QCheckBox(kbib, self)
            checker.setChecked(check_list[kbib])
            self.kbible_checker[kbib] = checker
            col = i % ncol
            row = row+1 if i is not 0 and i%ncol is 0 else row
            kbib_layout.addWidget(self.kbible_checker[kbib], row, col)
            
        kbib_group.setLayout(kbib_layout)
        layout.addRow(kbib_group)		
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
        file = QtGui.QFileDialog.getOpenFileName(self, "%s DB"%btn.kbib, directory=os.getcwd())
        if not file: return
        fpath, fname = os.path.split(file)
        
        self.kbible_file  [btn.kbib].setText(fname)
        self.kbible_path  [btn.kbib].setText(fpath)
       
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
    def save_kbible_path(self):
        try:
            with open(_kbible_path_file, "wt") as fo:
                keys = self.kbible_file.keys()
                for key in keys:
                    kf = self.kbible_file[key]
                    kp = self.kbible_path[key]
                    fo.write("%s,%s,%s\n" %(key, kp.text(), kf.text()))
        except Exception as e:
            self.message.appendPlainText('... Error ==> %s'%str(e))
            
    def load_kbible_path(self):
        try:
            with open(_kbible_path_file, "rt") as fr:
                for line in fr:
                    info = line.strip().split(',')
                    key = info[0].strip()
                    kp  = info[1].strip()
                    kf  = info[2].strip()
                    self.kbible_file[key].setText(kf)
                    self.kbible_path[key].setText(kp)
        except Exception as e:
            self.message.appendPlainText('... Error ==> %s'%str(e))   
        
    def apply_source_path_all(self):
        return
        
    def choose_output_folder(self):
        cur_path = os.getcwd() 
        path = QtGui.QFileDialog.getExistingDirectory(None, 'Save folder', cur_path, 
        QtGui.QFileDialog.ShowDirsOnly)
        if not path: return
        self.xref_output_path.setText(path)
        
    def confirm_db_check(self):
        check_list = bwxref.get_kbible_check_list()
        self.db_list = {}
        for key, checker in self.kbible_checker.items():
            #checker = self.kbible_checker[key]
            check_list[key] = checker.isChecked()
            if check_list[key] is True:
                self.db_list[key] = os.path.join(self.kbible_path[key].text(), 
                                                 self.kbible_file[key].text())
        
    def get_output_file(self):
        return os.path.join(self.xref_output_path.text(), self.xref_output.text())
        
    def xref_save_txt(self):
        self.message.appendPlainText('... xref to txt')
        self.confirm_db_check()
        #fn = "%s.txt"%self.get_output_file()
        path, file = self.xref_output_path.text(), self.xref_output.text()
        bwxref.xref_to_kor(path, file, self.xref_type_combo.currentText(),
                           bwxref.get_write_format_txt(), 
                           self.db_list, self.message)
        
    def xref_save_docx(self):
        self.message.appendPlainText('... xref to docx')
        self.confirm_db_check()
        #fn = "%s.docx"%self.get_output_file()
        path, file = self.xref_output_path.text(), self.xref_output.text()
        bwxref.xref_to_kor(path, file, self.xref_type_combo.currentText(), 
                           bwxref.get_write_format_docx(), 
                           self.db_list, self.message)
        
    def xref_save_html(self):
        self.message.appendPlainText('... xref to html')
        self.confirm_db_check()
        #fn = "%s.html"%self.get_output_file()
        path, file = self.xref_output_path.text(), self.xref_output.text()
        bwxref.xref_to_kor(path, file, self.xref_type_combo.currentText(), 
                           bwxref.get_write_format_html(), 
                           self.db_list, self.message)
        
def main(): 
    app = QtGui.QApplication(sys.argv)
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'Plastique'))
    run = XRefConvert()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
