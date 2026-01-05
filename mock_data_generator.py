import random

class MockDataGenerator:
    def __init__(self):
        self.popular_songs = {
            '周杰伦': [
                ('夜曲', '古风', '忧郁'),
                ('稻香', '民谣', '快乐'),
                ('青花瓷', '古风', '宁静'),
                ('双截棍', '说唱', '激昂'),
                ('简单爱', '流行', '浪漫'),
                ('告白气球', '流行', '浪漫'),
                ('菊花台', '古风', '忧郁'),
                ('东风破', '古风', '宁静'),
                ('龙拳', '说唱', '激昂'),
                ('晴天', '流行', '快乐')
            ],
            '林俊杰': [
                ('江南', '流行', '浪漫'),
                ('曹操', '流行', '激昂'),
                ('小酒窝', '流行', '快乐'),
                ('醉赤壁', '古风', '激昂'),
                ('背对背拥抱', '流行', '忧郁')
            ],
            '邓紫棋': [
                ('泡沫', '流行', '忧郁'),
                ('光年之外', '流行', '深沉'),
                ('来自天堂的魔鬼', '流行', '激昂'),
                ('画', '流行', '浪漫')
            ],
            '薛之谦': [
                ('演员', '流行', '忧郁'),
                ('认真的雪', '流行', '忧郁'),
                ('丑八怪', '流行', '自信'),
                ('刚刚好', '流行', '浪漫')
            ],
            '陈奕迅': [
                ('十年', '流行', '忧郁'),
                ('K歌之王', '流行', '激昂'),
                ('富士山下', '流行', '深沉'),
                ('爱情转移', '流行', '浪漫')
            ],
            '李荣浩': [
                ('李白', '流行', '自信'),
                ('模特', '流行', '快乐'),
                ('老街', '民谣', '忧郁'),
                ('年少有为', '流行', '深沉')
            ],
            '毛不易': [
                ('消愁', '民谣', '忧郁'),
                ('像我这样的人', '民谣', '深沉'),
                ('借', '民谣', '忧郁'),
                ('无问', '民谣', '宁静')
            ],
            '华晨宇': [
                ('齐天大圣', '摇滚', '激昂'),
                ('我管你', '摇滚', '自信'),
                ('好想爱这个世界啊', '流行', '快乐'),
                ('斗牛', '摇滚', '激昂')
            ]
        }
        
        self.genres = ['流行', '摇滚', '民谣', '电子', '古风', '说唱', '爵士', '古典', '蓝调']
        self.moods = ['快乐', '激昂', '忧郁', '兴奋', '宁静', '自信', '浪漫', '优雅', '深沉']
    
    def generate_playlist(self, platform='kugou', size=15):
        """生成模拟歌单"""
        songs = []
        
        # 随机选择一些热门歌手的歌曲
        selected_artists = random.sample(list(self.popular_songs.keys()), min(4, len(self.popular_songs)))
        
        for artist in selected_artists:
            artist_songs = self.popular_songs[artist]
            # 每个歌手选择2-4首歌
            num_songs = random.randint(2, min(4, len(artist_songs)))
            selected_songs = random.sample(artist_songs, num_songs)
            
            for title, genre, mood in selected_songs:
                songs.append({
                    'title': title,
                    'artist': artist,
                    'genre': genre,
                    'mood': mood,
                    'duration': random.randint(180, 300),  # 3-5分钟
                    'platform': platform
                })
        
        # 如果歌曲数量不够，添加一些随机歌曲
        while len(songs) < size:
            artist = random.choice(list(self.popular_songs.keys()))
            song_data = random.choice(self.popular_songs[artist])
            songs.append({
                'title': song_data[0],
                'artist': artist,
                'genre': song_data[1],
                'mood': song_data[2],
                'duration': random.randint(180, 300),
                'platform': platform
            })
        
        return songs[:size]
    
    def generate_diverse_playlist(self, size=20):
        """生成风格多样化的歌单"""
        songs = []
        
        # 确保包含各种风格
        genre_distribution = {
            '流行': 0.4,
            '民谣': 0.15,
            '古风': 0.15,
            '摇滚': 0.1,
            '说唱': 0.1,
            '其他': 0.1
        }
        
        for genre, ratio in genre_distribution.items():
            count = int(size * ratio)
            if genre == '其他':
                count = size - len(songs)  # 剩余的歌曲
            
            for _ in range(count):
                if genre == '其他':
                    selected_genre = random.choice(['电子', '爵士', '古典', '蓝调'])
                else:
                    selected_genre = genre
                
                # 根据流派选择合适的歌手和歌曲
                suitable_artists = []
                for artist, song_list in self.popular_songs.items():
                    for song_data in song_list:
                        if song_data[1] == selected_genre:
                            suitable_artists.append((artist, song_data))
                
                if suitable_artists:
                    artist, song_data = random.choice(suitable_artists)
                    songs.append({
                        'title': song_data[0],
                        'artist': artist,
                        'genre': song_data[1],
                        'mood': song_data[2],
                        'duration': random.randint(180, 300),
                        'platform': 'mock'
                    })
                else:
                    # 如果没有合适的歌曲，创建一个
                    artist = random.choice(list(self.popular_songs.keys()))
                    mood = random.choice(self.moods)
                    songs.append({
                        'title': f'模拟{selected_genre}歌曲',
                        'artist': artist,
                        'genre': selected_genre,
                        'mood': mood,
                        'duration': random.randint(180, 300),
                        'platform': 'mock'
                    })
        
        return songs