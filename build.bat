@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Vai para a pasta onde o BAT está localizado
cd /d "%~dp0"

echo ====================================
echo Filtro de Visao Confortavel
echo Lucas Andrade Desenvolvimento
echo ====================================
echo.

:: Verifica se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Instale Python em: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python encontrado!

:: Verifica se o arquivo Python existe
if not exist "comfort_vision_pro.py" (
    echo [ERRO] Arquivo comfort_vision_pro.py nao encontrado!
    pause
    exit /b 1
)
echo [OK] comfort_vision_pro.py encontrado!

:: Verifica se requirements existe
if not exist "requirements.txt" (
    echo [ERRO] Arquivo requirements.txt nao encontrado!
    pause
    exit /b 1
)
echo [OK] requirements.txt encontrado!
echo.

:: Verifica a logo
set LOGO_PATH=C:\Users\LucasRafaeldeAndrade\Downloads\Logo.png
if exist "!LOGO_PATH!" (
    echo [OK] Logo encontrada!
    set USE_ICON=YES
) else (
    echo [AVISO] Logo nao encontrada - continuando sem icone
    set USE_ICON=NO
)
echo.

:: Instala dependências
echo ====================================
echo [1/3] Instalando dependencias...
echo ====================================
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao instalar dependencias!
    pause
    exit /b 1
)
echo.
echo [OK] Dependencias instaladas!
echo.

:: Cria o executável
echo ====================================
echo [2/3] Criando executavel...
echo ====================================
echo Isso pode levar alguns minutos...
echo.

if "!USE_ICON!"=="YES" (
    pyinstaller --name="FiltroVisaoConfortavel" --onefile --windowed --icon="!LOGO_PATH!" --add-data="!LOGO_PATH!;." --hidden-import=PIL --hidden-import=pystray --hidden-import=pynput comfort_vision_pro.py
) else (
    pyinstaller --name="FiltroVisaoConfortavel" --onefile --windowed --hidden-import=PIL --hidden-import=pystray --hidden-import=pynput comfort_vision_pro.py
)

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao criar executavel!
    pause
    exit /b 1
)
echo.
echo [OK] Executavel criado!
echo.

:: Limpa arquivos temporários
echo ====================================
echo [3/3] Limpando arquivos temporarios...
echo ====================================
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"
echo [OK] Limpeza concluida!
echo.

:: Mensagem final
echo ====================================
echo COMPILACAO CONCLUIDA COM SUCESSO!
echo ====================================
echo.
echo Executavel criado em:
echo %CD%\dist\FiltroVisaoConfortavel.exe
echo.
echo Tamanho: ~60 MB
echo.
pause