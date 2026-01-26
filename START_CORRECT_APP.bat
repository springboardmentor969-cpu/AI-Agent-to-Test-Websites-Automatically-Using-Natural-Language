@echo off
echo ===============================================
echo  STARTING THE CORRECT STREAMLIT APP
echo ===============================================
echo.
echo Navigating to the correct project directory...
cd /d "d:\AI-powered testing agent Infofsys\aiwebtestingagent"
echo.
echo Current directory:
cd
echo.
echo Activating virtual environment...
call .\projenv310\Scripts\Activate.ps1
echo.
echo Clearing cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo.
echo Starting Streamlit with the UPDATED code...
echo.
echo ===============================================
streamlit run ui/app.py
pause
