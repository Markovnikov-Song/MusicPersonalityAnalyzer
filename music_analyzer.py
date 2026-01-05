import pandas as pd
from collections import Counter

class MusicAnalyzer:
    def __init__(self):
        # 音乐特征到性格维度的映射
        self.genre_personality_map = {
            '流行': {'E': 0.6, 'S': 0.7, 'F': 0.6, 'P': 0.5},
            '摇滚': {'E': 0.8, 'N': 0.6, 'T': 0.7, 'P': 0.6},
            '民谣': {'I': 0.7, 'N': 0.8, 'F': 0.8, 'J': 0.6},
            '电子': {'E': 0.7, 'N': 0.7, 'T': 0.6, 'P': 0.8},
            '古风': {'I': 0.6, 'S': 0.5, 'F': 0.7, 'J': 0.7},
            '说唱': {'E': 0.9, 'N': 0.6, 'T': 0.8, 'P': 0.7},
            '爵士': {'I': 0.6, 'N': 0.8, 'F': 0.6, 'P': 0.7},
            '古典': {'I': 0.8, 'N': 0.7, 'T': 0.6, 'J': 0.8},
            '蓝调': {'I': 0.7, 'N': 0.6, 'F': 0.8, 'P': 0.5}
        }
        
        self.mood_personality_map = {
            '快乐': {'E': 0.8, 'F': 0.7, 'P': 0.6},
            '激昂': {'E': 0.9, 'T': 0.6, 'P': 0.7},
            '忧郁': {'I': 0.8, 'N': 0.7, 'F': 0.8},
            '兴奋': {'E': 0.8, 'S': 0.6, 'P': 0.8},
            '宁静': {'I': 0.7, 'S': 0.5, 'J': 0.7},
            '自信': {'E': 0.7, 'T': 0.8, 'J': 0.6},
            '浪漫': {'F': 0.8, 'N': 0.6, 'P': 0.6},
            '优雅': {'I': 0.6, 'S': 0.7, 'J': 0.8},
            '深沉': {'I': 0.8, 'N': 0.8, 'T': 0.6}
        }
    
    def analyze_songs(self, songs):
        """分析歌曲列表，提取音乐特征"""
        if not songs:
            return {}
        
        # 统计流派分布
        genres = [song.get('genre', '未知') for song in songs]
        genre_counts = Counter(genres)
        
        # 统计情绪分布
        moods = [song.get('mood', '未知') for song in songs]
        mood_counts = Counter(moods)
        
        # 计算性格维度得分
        personality_scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
        total_weight = 0
        
        # 基于流派计算得分
        for genre, count in genre_counts.items():
            if genre in self.genre_personality_map:
                weight = count / len(songs)
                for dimension, score in self.genre_personality_map[genre].items():
                    personality_scores[dimension] += score * weight
                    total_weight += weight
        
        # 基于情绪计算得分
        for mood, count in mood_counts.items():
            if mood in self.mood_personality_map:
                weight = count / len(songs)
                for dimension, score in self.mood_personality_map[mood].items():
                    personality_scores[dimension] += score * weight
        
        # 标准化得分
        if total_weight > 0:
            for key in personality_scores:
                personality_scores[key] = personality_scores[key] / max(total_weight, 1)
        
        return {
            'genre_distribution': dict(genre_counts),
            'mood_distribution': dict(mood_counts),
            'personality_scores': personality_scores,
            'total_songs': len(songs)
        }