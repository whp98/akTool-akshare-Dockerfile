pyinstaller -D .\src\main.py --noconfirm
mkdir .\dist\main\akshare
copy-item .\Lib\site-packages\py_mini_racer\mini_racer.dll .\dist\main\mini_racer.dll
mkdir .\dist\main\akshare\file_fold
copy-item .\Lib\site-packages\akshare\file_fold\calendar.json .\dist\main\akshare\file_fold\calendar.json
