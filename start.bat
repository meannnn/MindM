@echo off
chcp 65001 >nul
title AI文档助手 - 启动中...

echo.
echo ========================================
echo    AI文档助手 v0.1.0
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.8+
    echo    下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python环境检查通过

:: 检查虚拟环境
if not exist "venv" (
    echo.
    echo 📦 创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo ✅ 虚拟环境创建成功
)

:: 激活虚拟环境
echo.
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 激活虚拟环境失败
    pause
    exit /b 1
)

:: 检查依赖包
echo.
echo 📋 检查依赖包...
pip list | findstr "Flask" >nul
if errorlevel 1 (
    echo 📥 安装依赖包...
    echo    正在安装基础依赖包...
    
    :: 逐个安装核心依赖包，避免编码问题
    pip install Flask==2.3.3
    pip install Werkzeug==2.3.7
    pip install python-docx==0.8.11
    pip install requests==2.31.0
    pip install python-dotenv==1.0.0
    pip install Pillow==10.0.1
    pip install colorlog==6.7.0
    pip install flask-cors==4.0.0
    
    if errorlevel 1 (
        echo ❌ 安装依赖包失败，尝试使用requirements.txt...
        pip install -r requirements.txt --no-cache-dir
        if errorlevel 1 (
            echo ❌ 依赖包安装失败
            echo    请手动安装依赖包或检查网络连接
            pause
            exit /b 1
        )
    )
    echo ✅ 依赖包安装完成
) else (
    echo ✅ 依赖包检查通过
)

:: 检查环境变量文件
if not exist ".env" (
    echo.
    echo ⚠️  警告: 未找到.env文件
    echo    请创建.env文件并配置您的API密钥
    echo    参考README.md中的配置说明
    echo.
    pause
)

:: 检查API密钥配置
if exist ".env" (
    findstr "DASHSCOPE_API_KEY=your_dashscope_api_key_here" .env >nul
    if not errorlevel 1 (
        echo.
        echo ⚠️  警告: 请配置您的阿里云百炼API密钥
        echo    编辑.env文件，设置DASHSCOPE_API_KEY
        echo.
    )
)

:: 创建必要的目录
echo.
echo 📁 创建必要目录...
if not exist "uploads" mkdir uploads
if not exist "outputs" mkdir outputs
if not exist "logs" mkdir logs
echo ✅ 目录创建完成

:: 启动应用
echo.
echo 🚀 启动AI文档助手...
echo.
echo ========================================
echo    服务启动中，请稍候...
echo    将自动打开浏览器
echo    按 Ctrl+C 停止服务
echo ========================================
echo.

:: 检查app.py是否存在
if not exist "app.py" (
    echo ❌ 错误: 未找到app.py文件
    echo    请确保项目文件完整
    pause
    exit /b 1
)

:: 检查start.py是否存在
if not exist "start.py" (
    echo ❌ 错误: 未找到start.py文件
    echo    请确保项目文件完整
    pause
    exit /b 1
)

:: 启动Flask应用
python start.py

:: 如果应用异常退出
echo.
echo ❌ 应用异常退出
pause