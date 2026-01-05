#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
发布脚本 - 自动化发布流程
"""

import os
import subprocess
import sys
import zipfile
import shutil
from datetime import datetime

def run_command(cmd, description):
    """运行命令并处理错误"""
    print(f"正在{description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description}成功")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败: {e}")
        print(f"错误输出: {e.stderr}")
        return None

def create_release_package():
    """创建发布包"""
    print("创建发布包...")
    
    # 创建发布目录
    release_dir = f"release-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    os.makedirs(release_dir, exist_ok=True)
    
    # 需要包含的文件
    files_to_include = [
        'app.py',
        'playlist_importer.py',
        'music_analyzer.py',
        'mbti_predictor.py',
        'kugou_api.py',
        'mock_data_generator.py',
        'config.py',
        'requirements.txt',
        'start.bat',
        'README.md',
        'LICENSE',
        'CHANGELOG.md',
        '.env'
    ]
    
    # 复制文件
    for file in files_to_include:
        if os.path.exists(file):
            shutil.copy2(file, release_dir)
            print(f"  ✅ 复制 {file}")
    
    # 复制templates目录
    if os.path.exists('templates'):
        shutil.copytree('templates', os.path.join(release_dir, 'templates'))
        print("  ✅ 复制 templates/")
    
    # 创建ZIP包
    zip_name = f"{release_dir}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, arc_name)
    
    print(f"✅ 发布包已创建: {zip_name}")
    return zip_name

def create_github_release_info():
    """创建GitHub发布信息"""
    release_notes = f"""# 音乐性格分析器 v1.0.0

## 🎯 主要功能
- 支持多平台歌单导入（网易云音乐、QQ音乐、酷狗音乐）
- 智能音乐风格和情绪分析
- MBTI性格类型预测
- 美观的Web用户界面

## 🚀 快速开始

### 方法一：下载源码包
1. 下载 `music-personality-analyzer-v1.0.0.zip`
2. 解压到任意目录
3. 双击运行 `start.bat`（Windows）或运行 `python app.py`
4. 浏览器访问 http://localhost:5000

### 方法二：使用Git克隆
```bash
git clone https://github.com/yourusername/music-personality-analyzer.git
cd music-personality-analyzer
pip install -r requirements.txt
python app.py
```

## 📋 系统要求
- Python 3.7+
- Windows/macOS/Linux
- 现代浏览器

## 🔧 依赖包
- Flask 3.1.2
- requests 2.32.5
- pandas 2.3.3
- scikit-learn 1.8.0
- beautifulsoup4 4.14.2

## 📝 更新日志
查看 [CHANGELOG.md](CHANGELOG.md) 了解详细更新内容。

## 🤝 贡献
欢迎提交Issue和Pull Request！

## 📄 许可证
MIT License - 查看 [LICENSE](LICENSE) 文件了解详情。
"""
    
    with open('RELEASE_NOTES.md', 'w', encoding='utf-8') as f:
        f.write(release_notes)
    
    print("✅ GitHub发布说明已创建: RELEASE_NOTES.md")

def main():
    """主函数"""
    print("🚀 音乐性格分析器 - 发布工具")
    print("=" * 50)
    
    # 检查Git状态
    git_status = run_command("git status --porcelain", "检查Git状态")
    if git_status and git_status.strip():
        print("⚠️  检测到未提交的更改，建议先提交所有更改")
        if input("是否继续？(y/N): ").lower() != 'y':
            return
    
    # 创建发布包
    zip_file = create_release_package()
    
    # 创建GitHub发布信息
    create_github_release_info()
    
    print("\n🎉 发布准备完成！")
    print("\n📦 发布文件:")
    print(f"  - {zip_file}")
    print("  - RELEASE_NOTES.md")
    
    print("\n📋 下一步操作:")
    print("1. 上传到GitHub:")
    print("   git add .")
    print("   git commit -m 'Release v1.0.0'")
    print("   git tag v1.0.0")
    print("   git push origin main --tags")
    
    print("\n2. 创建GitHub Release:")
    print("   - 访问GitHub仓库页面")
    print("   - 点击 'Releases' -> 'Create a new release'")
    print("   - 选择标签 v1.0.0")
    print(f"   - 上传 {zip_file}")
    print("   - 复制 RELEASE_NOTES.md 内容到描述")
    
    print("\n3. 发布到PyPI (可选):")
    print("   python setup.py sdist bdist_wheel")
    print("   pip install twine")
    print("   twine upload dist/*")

if __name__ == "__main__":
    main()