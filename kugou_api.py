import requests
import json
import re
from urllib.parse import quote
import time

class KugouAPI:
    def __init__(self):
        self.base_url = "http://m.kugou.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'http://m.kugou.com/'
        }
        
    def get_playlist_info(self, playlist_id):
        """获取歌单信息"""
        try:
            url = f"{self.base_url}/plist/list/{playlist_id}?json=true"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('list', {})
            return None
        except Exception as e:
            print(f"获取酷狗歌单信息失败: {e}")
            return None
    
    def get_playlist_songs(self, playlist_id, page=1):
        """获取歌单歌曲列表"""
        try:
            url = f"{self.base_url}/plist/list/{playlist_id}?json=true&page={page}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                songs = []
                
                if 'list' in data and 'list' in data['list']:
                    for item in data['list']['list']:
                        song_info = self._parse_song_info(item)
                        if song_info:
                            songs.append(song_info)
                
                return songs
            return []
        except Exception as e:
            print(f"获取酷狗歌单歌曲失败: {e}")
            return []
    
    def search_songs(self, keyword, page=1, pagesize=20):
        """搜索歌曲"""
        try:
            encoded_keyword = quote(keyword)
            url = f"{self.base_url}/api/v3/search/song"
            params = {
                'format': 'json',
                'keyword': encoded_keyword,
                'page': page,
                'pagesize': pagesize,
                'showtype': 1
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                songs = []
                
                if 'data' in data and 'info' in data['data']:
                    for item in data['data']['info']:
                        song_info = self._parse_search_result(item)
                        if song_info:
                            songs.append(song_info)
                
                return songs
            return []
        except Exception as e:
            print(f"搜索酷狗歌曲失败: {e}")
            return []
    
    def get_song_detail(self, hash_value):
        """获取歌曲详细信息"""
        try:
            url = f"{self.base_url}/app/i/getSongInfo.php"
            params = {
                'cmd': 'playInfo',
                'hash': hash_value
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data
            return None
        except Exception as e:
            print(f"获取酷狗歌曲详情失败: {e}")
            return None
    
    def _parse_song_info(self, item):
        """解析歌曲信息"""
        try:
            # 从文件名中提取歌手和歌曲名
            filename = item.get('filename', '')
            if ' - ' in filename:
                parts = filename.split(' - ', 1)
                artist = parts[0].strip()
                title = parts[1].strip()
            else:
                artist = "未知歌手"
                title = filename
            
            # 根据歌曲名和歌手推测流派和情绪
            genre, mood = self._analyze_music_style(title, artist)
            
            return {
                'title': title,
                'artist': artist,
                'genre': genre,
                'mood': mood,
                'duration': item.get('duration', 0),
                'hash': item.get('hash', ''),
                'filesize': item.get('filesize', 0)
            }
        except Exception as e:
            print(f"解析歌曲信息失败: {e}")
            return None
    
    def _parse_search_result(self, item):
        """解析搜索结果"""
        try:
            title = item.get('songname', '').strip()
            artist = item.get('singername', '').strip()
            
            # 根据歌曲名和歌手推测流派和情绪
            genre, mood = self._analyze_music_style(title, artist)
            
            return {
                'title': title,
                'artist': artist,
                'genre': genre,
                'mood': mood,
                'duration': item.get('duration', 0),
                'hash': item.get('hash', ''),
                'album_name': item.get('album_name', '')
            }
        except Exception as e:
            print(f"解析搜索结果失败: {e}")
            return None
    
    def _analyze_music_style(self, title, artist):
        """基于歌曲名和歌手分析音乐风格和情绪"""
        title_lower = title.lower()
        artist_lower = artist.lower()
        
        # 流派判断关键词
        genre_keywords = {
            '民谣': ['故乡', '远方', '时光', '青春', '回忆', '民谣', '稻香', '童话'],
            '古风': ['古风', '江湖', '侠客', '红尘', '天涯', '古典', '青花瓷', '东风破'],
            '说唱': ['rap', 'hip hop', '说唱', '嘻哈', '双截棍', '龙拳'],
            '摇滚': ['rock', '摇滚', '叛逆', '自由', '疯狂', '老男孩'],
            '电子': ['electronic', 'edm', '电子', '节拍'],
            '爵士': ['jazz', '爵士', '蓝调', 'blues'],
            '古典': ['古典', 'classical', '交响', '协奏'],
            '蓝调': ['blues', '蓝调', '忧郁', '夜曲'],
            '流行': ['爱', '心', '梦', '想', '情', '恋', '你', '我', '简单']
        }
        
        # 情绪判断关键词
        mood_keywords = {
            '忧郁': ['忧伤', '孤独', '思念', '离别', '眼泪', '痛', '夜曲', '黑色'],
            '快乐': ['快乐', '开心', '欢乐', '阳光', '笑', '甜蜜', '稻香', '简单爱'],
            '宁静': ['宁静', '安静', '平静', '温柔', '轻柔', '青花瓷', '菊花台'],
            '激昂': ['激情', '热血', '奋斗', '拼搏', '战斗', '力量', '双截棍', '龙拳'],
            '浪漫': ['浪漫', '温馨', '甜蜜', '约会', '情人', '告白气球', '简单爱'],
            '兴奋': ['兴奋', '狂欢', '派对', '疯狂', '激动'],
            '自信': ['自信', '强大', '无敌', '王者', '霸气'],
            '优雅': ['优雅', '高贵', '典雅', '精致'],
            '深沉': ['深沉', '沉重', '哲理', '思考', '内省', '老男孩']
        }
        
        # 默认值
        genre = '流行'
        mood = '快乐'
        
        # 判断流派 - 按优先级排序
        for g, keywords in genre_keywords.items():
            if any(keyword in title_lower or keyword in artist_lower for keyword in keywords):
                genre = g
                break
        
        # 判断情绪
        for m, keywords in mood_keywords.items():
            if any(keyword in title_lower or keyword in artist_lower for keyword in keywords):
                mood = m
                break
        
        return genre, mood