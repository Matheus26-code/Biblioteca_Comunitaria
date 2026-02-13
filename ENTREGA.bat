@echo off
title SISTEMA BIBLIOTECA - INICIANDO
:: O comando abaixo entra na pasta onde o arquivo .bat está salvo
cd /d "%~dp0"
echo Pasta atual: %cd%
echo Verificando arquivo app.py...
if exist app.py (
    python app.py
) else (
    echo ERRO: Arquivo app.py nao encontrado nesta pasta!
    echo Certifique-se de que o .bat esta dentro da pasta biblioteca_comunitaria.
)
pause