@set ANACONDA_PATH=C:\Users\Administrator\Anaconda3
@set PATH=%PATH%;%ANACONDA_PATH%;%ANACONDA_PATH%\Scripts;%ANACONDA_PATH%\Library\bin
python .\mysite\manage.py runserver
cmd /k