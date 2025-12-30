@echo off
REM PX4 SITL Windows启动脚本
REM 用于在Windows WSL或原生环境中启动PX4仿真

echo =======================================
echo     PX4 SITL Windows启动脚本
echo =======================================

REM 检查是否在WSL中
wsl --list >nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: 未检测到WSL
    echo 请确保在WSL Ubuntu环境中运行此脚本
    echo 或者直接在Ubuntu中运行 start_px4_sitl.sh
    pause
    exit /b 1
)

REM 检查PX4目录
set PX4_DIR=%USERPROFILE%\px4_ws\PX4-Autopilot
if not exist "%PX4_DIR%" (
    echo 错误: PX4目录不存在: %PX4_DIR%
    echo 请先按照 PX4_SITL_SETUP.md 安装PX4
    echo.
    echo 如果PX4在其他位置，请修改脚本中的PX4_DIR变量
    pause
    exit /b 1
)

echo 进入PX4目录: %PX4_DIR%

REM 检查是否已经运行
tasklist /FI "IMAGENAME eq px4.exe" 2>NUL | find /I /N "px4.exe">NUL
if %ERRORLEVEL% EQU 0 (
    echo 警告: 发现PX4进程正在运行
    set /p choice="是否要停止现有进程并重新启动? (y/n): "
    if /i "!choice!"=="y" (
        taskkill /F /IM px4.exe /T 2>nul
        timeout /t 2 /nobreak >nul
    ) else (
        echo 退出启动脚本
        pause
        exit /b 0
    )
)

echo.
echo 选择仿真器:
echo 1) Gazebo (推荐，有GUI)
echo 2) jmavsim (轻量，无GUI)
set /p sim_choice="请输入选择 (1或2): "

if "%sim_choice%"=="1" (
    set SIMULATOR=gazebo
) else if "%sim_choice%"=="2" (
    set SIMULATOR=jmavsim
) else (
    echo 无效选择，使用Gazebo
    set SIMULATOR=gazebo
)

echo.
echo 选择机架类型:
echo 1) 四旋翼 (iris) - 默认
echo 2) 固定翼 (plane)
echo 3) rover (地面车辆)
set /p vehicle_choice="请输入选择 (1-3): "

if "%vehicle_choice%"=="1" (
    set VEHICLE=
) else if "%vehicle_choice%"=="2" (
    set VEHICLE=_plane
) else if "%vehicle_choice%"=="3" (
    set VEHICLE=_rover
) else (
    set VEHICLE=
)

REM 构建WSL命令
set WSL_COMMAND=wsl bash -c "cd '%PX4_DIR:\=/%' && make px4_sitl %SIMULATOR%%VEHICLE%"

echo.
echo 执行命令: %WSL_COMMAND%
echo =======================================

REM 执行命令
%WSL_COMMAND%

echo.
echo =======================================
echo PX4 SITL 已停止
pause
