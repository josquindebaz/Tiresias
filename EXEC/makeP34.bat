del TiresiasP34.zip
mkdir Tiresias
"C:\Python34\Scripts\pyinstaller.exe"  -y --clean --onefile --distpath Tiresias "..\Tiresias.py"
rd /S /Q build
xcopy "..\README.md" Tiresias /Y /D /K 
xcopy "..\CHANGELOG.txt" Tiresias /Y /D /K  
xcopy "..\param.json" Tiresias /Y /D /K  
xcopy "..\frm" "Tiresias\data\" /Y /E /D /I /K  
xcopy "..\data" "Tiresias\data\" /Y /E /D /I /K   
"c:\Program Files\7-Zip\7z.exe" u TiresiasP34.zip Tiresias
rd /S /Q Tiresias
del Tiresias.spec
