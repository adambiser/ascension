@ECHO OFF
pyinstaller onedir.spec
rmdir /s /q build
robocopy "dist\Ascension-win64" "dist\Ascension-win64\lib" *.* /mov /xf *.exe base_library.zip python3*.dll icon.ico credits.txt
pause
