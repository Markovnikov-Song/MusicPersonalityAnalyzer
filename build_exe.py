#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PyInstaller打包脚本
用于创建独立的可执行文件
"""

import os
import sys
import subprocess
import shutil

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_spec_file():
    """创建PyInstaller配置文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('README.md', '.'),
        ('requirements.txt', '.'),
        ('.env', '.'),
    ],
    hiddenimports=[
        'flask',
        'requests',
        'pandas',
        'sklearn',
        'numpy',
        'bs4',
        'lxml',
        'dotenv'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MusicPersonalityAnalyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('music_analyzer.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("已创建 music_analyzer.spec 文件")

def build_executable():
    """构建可执行文件"""
    print("正在构建可执行文件...")
    
    # 清理之前的构建
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # 运行PyInstaller
    subprocess.check_call(['pyinstaller', 'music_analyzer.spec', '--clean'])
    
    print("构建完成！可执行文件位于 dist/ 目录")

def create_installer_script():
    """创建安装脚本"""
    installer_content = '''@echo off
echo 音乐性格分析器 - 安装程序
echo ================================

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.7+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 正在安装依赖包...
pip install -r requirements.txt

echo 安装完成！
echo.
echo 使用方法：
echo 1. 双击 start.bat 启动应用
echo 2. 或运行命令：python app.py
echo 3. 浏览器访问：http://localhost:5000
echo.
pause
'''
    
    with open('install.bat', 'w', encoding='utf-8') as f:
        f.write(installer_content)
    
    print("已创建 install.bat 安装脚本")

def main():
    """主函数"""
    print("音乐性格分析器 - 打包工具")
    print("=" * 40)
    
    choice = input("请选择打包方式：\n1. 创建Python安装包\n2. 创建独立可执行文件\n3. 创建安装脚本\n请输入选择 (1-3): ")
    
    if choice == '1':
        print("创建Python安装包...")
        subprocess.check_call([sys.executable, "setup.py", "sdist", "bdist_wheel"])
        print("安装包已创建在 dist/ 目录")
        
    elif choice == '2':
        try:
            install_pyinstaller()
            create_spec_file()
            build_executable()
        except Exception as e:
            print(f"构建失败：{e}")
            
    elif choice == '3':
        create_installer_script()
        print("安装脚本已创建")
        
    else:
        print("无效选择")

if __name__ == "__main__":
    main()
'''