@echo off
set /a r=%random% %%%2 +%1
echo %r% > %3