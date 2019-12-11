del Tiresias.zip
mkdir Tiresias
"C:\Users\gspr\AppData\Local\Programs\Python\Python37-32\Scripts\pyinstaller.exe"  -y --clean --onefile --distpath Tiresias "..\Tiresias.py"
rd /S /Q build
xcopy "..\README.md" Tiresias /Y /D /K 
xcopy "..\CHANGELOG.txt" Tiresias /Y /D /K  
xcopy "..\param.json" Tiresias /Y /D /K  
xcopy "..\data" "Tiresias\data\" /Y /E /D /I /K   
"c:\Program Files\7-Zip\7z.exe" u Tiresias.zip Tiresias
rd /S /Q Tiresias
del Tiresias.spec
