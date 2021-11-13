pyinstaller --onefile -w Swap!.py
mkdir dist\levels
mkdir dist\logic
mkdir dist\saves
mkdir dist\sprites
mkdir "dist\menu sprites"
xcopy levels dist\levels /E
xcopy logic dist\logic /E
xcopy saves dist\saves /E
xcopy sprites dist\sprites /E
xcopy sprites "dist\menu sprites" /E
copy config dist
rename dist Swap!