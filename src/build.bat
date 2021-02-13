del .\XRef\Xref.exe
del .\XRef\library.zip

python setup.py build

copy /y kbible_list.txt .\XRef
copy /y kbible_path.txt .\XRef
copy /y ebible_list.txt .\XRef
copy /y ebible_path.txt .\XRef

copy /y default.docx .\XRef
copy /y default-settings.xml .\XRef

