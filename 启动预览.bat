@echo off
title 个人笔记网站 - 本地预览
color 0A

echo ========================================
echo   个人笔记网站 - 本地预览
echo ========================================
echo.

cd /d "%~dp0"

echo 正在自动生成配置文件...
python build-config.py
if errorlevel 1 (
    echo 错误: 配置生成失败，请检查 Python 是否安装
    pause
    exit /b 1
)
echo 配置生成成功！
echo.

echo 启动本地服务器...
echo 访问地址: http://localhost:8080
echo 按 Ctrl+C 停止服务器
echo.

start "" "http://localhost:8080"
python -m http.server 8080

pause