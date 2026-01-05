import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # 音乐平台API配置
    NETEASE_API_KEY = os.environ.get('NETEASE_API_KEY')
    QQ_MUSIC_API_KEY = os.environ.get('QQ_MUSIC_API_KEY')
    KUGOU_API_KEY = os.environ.get('KUGOU_API_KEY')
    
    # MBTI分析配置
    MIN_SONGS_FOR_ANALYSIS = 5  # 最少需要的歌曲数量
    CONFIDENCE_THRESHOLD = 0.6  # 置信度阈值
    
    # 请求配置
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3