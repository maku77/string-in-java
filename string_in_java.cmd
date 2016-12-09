@echo off
setlocal
set script="%~dp0%string_in_java.py"
python %script% %*
endlocal
