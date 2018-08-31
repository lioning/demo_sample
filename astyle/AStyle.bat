REM All CPP source file will be modified by AStyle
REM 2009-01-05
REM set up astyle.exe
@echo off
set astyle="astyle.exe"
REM iterate folders
:: for /r . %%a in (*.cpp;*.c) do ::recursive
for  %%a in (*.cpp;*.c) do %astyle% --style=ansi --pad-oper --unpad-paren -s4 --indent-namespaces -n "%%a"
for  %%a in (*.hpp;*.h) do %astyle% --style=ansi --pad-oper --unpad-paren -s4 --indent-namespaces -n "%%a"
REM Delete .orig file
for /r . %%a in (*.orig) do del "%%a"
pause