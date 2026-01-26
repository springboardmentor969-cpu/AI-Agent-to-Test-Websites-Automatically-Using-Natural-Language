@echo off
echo ===============================================
echo  COMPLETE STREAMLIT RESET
echo ===============================================
echo.

echo [1/4] Stopping any running Streamlit processes...
taskkill /F /IM streamlit.exe 2>nul
timeout /t 2 /nobreak >nul

echo [2/4] Clearing Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul

echo [3/4] Clearing Streamlit cache...
if exist "%USERPROFILE%\.streamlit" (
    del /s /q "%USERPROFILE%\.streamlit\cache" 2>nul
)

echo [4/4] Starting Streamlit...
echo.
echo ===============================================
echo  Starting fresh Streamlit instance...
echo ===============================================
echo.

call .\projenv310\Scripts\Activate.ps1
streamlit run ui/app.py

pause
