pyinstaller --onefile -w Editor.py
mkdir dist\levels
mkdir dist\logic
mkdir dist\sprites
xcopy sprites dist\sprites /E
rename dist "Level Editor"