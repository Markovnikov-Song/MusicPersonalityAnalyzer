from flask import Flask, render_template, request, jsonify
from music_analyzer import MusicAnalyzer
from playlist_importer import PlaylistImporter
from mbti_predictor import MBTIPredictor
import os

app = Flask(__name__)

# 初始化组件
playlist_importer = PlaylistImporter()
music_analyzer = MusicAnalyzer()
mbti_predictor = MBTIPredictor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_playlist():
    try:
        data = request.json
        playlist_url = data.get('playlist_url')
        
        if not playlist_url:
            return jsonify({'error': '请提供歌单链接'}), 400
        
        # 导入歌单
        songs = playlist_importer.import_playlist(playlist_url)
        if not songs:
            return jsonify({'error': '无法导入歌单，请检查链接是否正确'}), 400
        
        # 分析音乐特征
        music_features = music_analyzer.analyze_songs(songs)
        
        # 预测MBTI
        mbti_result = mbti_predictor.predict(music_features)
        
        return jsonify({
            'success': True,
            'songs_count': len(songs),
            'mbti_type': mbti_result['type'],
            'confidence': mbti_result['confidence'],
            'analysis': mbti_result['analysis'],
            'features': music_features
        })
        
    except Exception as e:
        return jsonify({'error': f'分析过程中出现错误: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

def main():
    """命令行入口点"""
    import webbrowser
    import threading
    import time
    
    def open_browser():
        time.sleep(1.5)  # 等待服务器启动
        webbrowser.open('http://localhost:5000')
    
    # 在后台线程中打开浏览器
    threading.Thread(target=open_browser, daemon=True).start()
    
    print("🎵 音乐性格分析器启动中...")
    print("📱 浏览器将自动打开，或手动访问: http://localhost:5000")
    print("⏹️  按 Ctrl+C 停止服务器")
    
    app.run(debug=False, host='0.0.0.0', port=5000)