pyinstaller --onefile -w Swap!.py
mkdir dist\levels
mkdir dist\logic
mkdir dist\saves
mkdir dist\sprites
xcopy levels dist\levels /E
xcopy logic dist\logic /E
xcopy saves dist\saves /E
xcopy sprites dist\sprites /E
rename dist Swap!