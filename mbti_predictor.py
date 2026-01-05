class MBTIPredictor:
    def __init__(self):
        self.mbti_descriptions = {
            'INTJ': '建筑师 - 富有想象力和战略性的思想家，一切皆在计划之中',
            'INTP': '逻辑学家 - 具有创造性的思想家，对知识有着不可抑制的渴望',
            'ENTJ': '指挥官 - 大胆，富有想象力，意志强烈的领导者',
            'ENTP': '辩论家 - 聪明好奇的思想家，不会放弃任何智力挑战',
            'INFJ': '提倡者 - 安静而神秘，同时鼓舞人心且不知疲倦的理想主义者',
            'INFP': '调停者 - 诗意，善良和利他主义，总是热切地想要帮助好的事业',
            'ENFJ': '主人公 - 富有魅力鼓舞人心的领导者，有能力让听众着迷',
            'ENFP': '竞选者 - 热情，有创造力，社交能力强，总是能找到笑的理由',
            'ISTJ': '物流师 - 实用主义和注重事实，可靠性无人能及',
            'ISFJ': '守卫者 - 非常专注和温暖的守护者，时刻准备保护爱的人',
            'ESTJ': '总经理 - 出色的管理者，在管理事情或人的时候无与伦比',
            'ESFJ': '执政官 - 极有同情心，受欢迎，总是热心帮助他人',
            'ISTP': '鉴赏家 - 大胆而实际的实验家，擅长使用各种工具',
            'ISFP': '探险家 - 灵活有魅力的艺术家，时刻准备探索新的可能性',
            'ESTP': '企业家 - 聪明，精力充沛，非常善于感知，真正享受生活在边缘',
            'ESFP': '娱乐家 - 自发的，精力充沛和热情的人，生活永远不会无聊'
        }
    
    def predict(self, music_features):
        """基于音乐特征预测MBTI类型"""
        if not music_features or 'personality_scores' not in music_features:
            return {
                'type': 'ISFP',
                'confidence': 0.5,
                'analysis': '数据不足，无法准确分析'
            }
        
        scores = music_features['personality_scores']
        
        # 确定每个维度
        e_i = 'E' if scores.get('E', 0) > scores.get('I', 0) else 'I'
        s_n = 'S' if scores.get('S', 0) > scores.get('N', 0) else 'N'
        t_f = 'T' if scores.get('T', 0) > scores.get('F', 0) else 'F'
        j_p = 'J' if scores.get('J', 0) > scores.get('P', 0) else 'P'
        
        mbti_type = e_i + s_n + t_f + j_p
        
        # 计算置信度
        confidence = self._calculate_confidence(scores)
        
        # 生成分析报告
        analysis = self._generate_analysis(mbti_type, music_features)
        
        return {
            'type': mbti_type,
            'confidence': confidence,
            'analysis': analysis,
            'description': self.mbti_descriptions.get(mbti_type, '未知类型')
        }
    
    def _calculate_confidence(self, scores):
        """计算预测置信度"""
        # 基于各维度得分差异计算置信度
        differences = []
        differences.append(abs(scores.get('E', 0) - scores.get('I', 0)))
        differences.append(abs(scores.get('S', 0) - scores.get('N', 0)))
        differences.append(abs(scores.get('T', 0) - scores.get('F', 0)))
        differences.append(abs(scores.get('J', 0) - scores.get('P', 0)))
        
        avg_difference = sum(differences) / len(differences)
        confidence = min(0.5 + avg_difference, 0.95)
        
        return round(confidence, 2)
    
    def _generate_analysis(self, mbti_type, features):
        """生成详细的性格分析"""
        genre_dist = features.get('genre_distribution', {})
        mood_dist = features.get('mood_distribution', {})
        
        analysis = f"基于您的音乐偏好分析，您的MBTI类型可能是 {mbti_type}。\n\n"
        
        # 分析音乐风格偏好
        if genre_dist:
            top_genre = max(genre_dist, key=genre_dist.get)
            analysis += f"您最喜欢的音乐风格是{top_genre}，"
            
            if top_genre in ['摇滚', '说唱']:
                analysis += "这表明您可能比较外向和直接。"
            elif top_genre in ['民谣', '古典']:
                analysis += "这表明您可能比较内向和深思。"
            elif top_genre in ['流行', '电子']:
                analysis += "这表明您可能喜欢跟上时代潮流。"
        
        analysis += "\n\n"
        
        # 分析情绪偏好
        if mood_dist:
            top_mood = max(mood_dist, key=mood_dist.get)
            analysis += f"您的音乐情绪偏好主要是{top_mood}，这反映了您的内在性格特质。"
        
        return analysis