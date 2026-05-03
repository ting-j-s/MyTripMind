"""
扩充日记数据
目标：≥20篇日记
"""

DIARIES = [
    {"user_id": "user_001", "title": "故宫一日游", "location_id": "ATTR_BJ_001", "content": "今天去了故宫，感受到了古代皇家的威严。建筑精美，文化底蕴深厚。建议早点去，人少一些。", "view_count": 520, "ratings": [5.0, 4.5, 4.8]},
    {"user_id": "user_002", "title": "颐和园春游记", "location_id": "ATTR_BJ_004", "content": "春天的颐和园太美了！湖面波光粼粼，柳树发芽，万寿山上的风景绝美。推荐划船游湖。", "view_count": 380, "ratings": [4.8, 5.0]},
    {"user_id": "user_003", "title": "长城脚下的一天", "location_id": "ATTR_BJ_006", "content": "八达岭长城不愧是天下第一关！爬上去虽然累，但看到壮观的景色一切都值了。注意防晒和带水。", "view_count": 680, "ratings": [5.0, 5.0, 4.5]},
    {"user_id": "user_001", "title": "天坛公园晨练", "location_id": "ATTR_BJ_003", "content": "早上六点来到天坛，很多大爷大妈在锻炼。祈年殿非常壮观，回音壁也很有意思。本地人推荐！", "view_count": 290, "ratings": [4.5, 4.3]},
    {"user_id": "user_004", "title": "北大校园漫步", "location_id": "ATTR_BJ_008", "content": "未名湖边的风景真美，博雅塔倒映在湖面上。校园里古建筑与现代建筑交相辉映，不愧是顶级学府。", "view_count": 450, "ratings": [4.8, 4.7, 5.0]},
    {"user_id": "user_005", "title": "清华园半日游", "location_id": "ATTR_BJ_009", "content": "水木清华，名不虚传。荷园池塘里的荷花正开，大礼堂前的草坪很适合休息。学霸们的校园真美。", "view_count": 410, "ratings": [4.6, 4.8]},
    {"user_id": "user_006", "title": "国家博物馆参观记", "location_id": "ATTR_BJ_017", "content": "国博真的很大，一天都看不完。古代中国展厅最震撼，青铜器精美绝伦。免费参观，但要提前预约。", "view_count": 360, "ratings": [4.9, 5.0, 4.8]},
    {"user_id": "user_007", "title": "鸟巢水立方夜景", "location_id": "ATTR_BJ_048", "content": "晚上的鸟巢和水立方太美了！灯光秀流光溢彩。周边很多人在拍照，是北京打卡必去之地。", "view_count": 580, "ratings": [4.7, 4.8, 4.9]},
    {"user_id": "user_008", "title": "南锣鼓巷淘宝", "location_id": "ATTR_BJ_033", "content": "南锣鼓巷是文艺青年的天堂！胡同里有各种特色小店，创意商品琳琅满目。巷子深处的咖啡馆很适合休息。", "view_count": 420, "ratings": [4.5, 4.6, 4.4]},
    {"user_id": "user_009", "title": "北海公园泛舟", "location_id": "ATTR_BJ_027", "content": "小时候学过让我们荡起双桨，今天终于在北海公园实现了！白塔就在湖边，景色太美了。", "view_count": 330, "ratings": [4.6, 4.5]},
    {"user_id": "user_010", "title": "香山红叶之旅", "location_id": "ATTR_BJ_034", "content": "秋天的香山满山红叶，层林尽染。爬到香炉峰俯瞰北京城，心旷神怡。体力不好的可以坐缆车。", "view_count": 510, "ratings": [4.8, 4.9, 5.0]},
    {"user_id": "user_001", "title": "圆明园怀古", "location_id": "ATTR_BJ_005", "content": "走进圆明园遗址，心情沉重。残垣断壁诉说着历史。提醒我们勿忘国耻，振兴中华。", "view_count": 440, "ratings": [4.7, 4.8]},
    {"user_id": "user_002", "title": "798艺术区探秘", "location_id": "ATTR_BJ_044", "content": "798艺术区太文艺了！各种当代艺术展览目不暇接。工业风格建筑和艺术作品完美融合，拍照超好看。", "view_count": 370, "ratings": [4.6, 4.5, 4.7]},
    {"user_id": "user_003", "title": "王府井小吃街觅食", "location_id": "ATTR_BJ_019", "content": "王府井小吃街美食太多了！炸灌肠、爆肚、糖葫芦...各种老北京小吃应有尽有。晚上去更有氛围。", "view_count": 490, "ratings": [4.4, 4.5, 4.3]},
    {"user_id": "user_004", "title": "天安门广场看升旗", "location_id": "ATTR_BJ_002", "content": "凌晨四点起床排队，只为看升旗仪式。当五星红旗升起的那一刻，自豪感油然而生。建议提前预约。", "view_count": 620, "ratings": [5.0, 5.0, 4.9]},
    {"user_id": "user_005", "title": "北京动物园亲子游", "location_id": "ATTR_BJ_055", "content": "带孩子来北京动物园看大熊猫！熊猫馆人气最旺。动物种类很多，建议坐游览车否则太累了。", "view_count": 350, "ratings": [4.5, 4.6]},
    {"user_id": "user_006", "title": "雍和宫祈福", "location_id": "ATTR_BJ_022", "content": "雍和宫是北京最灵验的寺庙之一。建筑金碧辉煌，香火旺盛。据说求学业很灵验，学生党必去。", "view_count": 400, "ratings": [4.6, 4.7, 4.5]},
    {"user_id": "user_007", "title": "后海酒吧街夜生活", "location_id": "ATTR_BJ_032", "content": "什刹海的夜晚灯火阑珊，酒吧一条街热闹非凡。坐在湖边喝一杯，听着歌手弹唱，太惬意了。", "view_count": 460, "ratings": [4.4, 4.5, 4.6]},
    {"user_id": "user_008", "title": "前门大街逛老字号", "location_id": "ATTR_BJ_037", "content": "前门大街保留了很多老字号，全聚德烤鸭、都一处烧麦...漫步在古街上感受老北京的韵味。", "view_count": 380, "ratings": [4.5, 4.4, 4.6]},
    {"user_id": "user_009", "title": "玉渊潭公园赏樱花", "location_id": "ATTR_BJ_030", "content": "春天来玉渊潭看樱花！满园的樱花盛开，粉白色的花海太浪漫了。很多人在野餐，氛围超好。", "view_count": 430, "ratings": [4.8, 4.7, 4.9]},
    {"user_id": "user_010", "title": "大栅栏感受老北京", "location_id": "ATTR_BJ_038", "content": "大栅栏是老北京最热闹的商业街，同仁堂、内联升...百年老店林立。晚上的红灯笼特别有年味。", "view_count": 340, "ratings": [4.5, 4.4]},
    {"user_id": "user_001", "title": "中山公园赏花", "location_id": "ATTR_BJ_028", "content": "中山公园每年春天的花展都很惊艳！郁金香、桃花、牡丹...各种花卉争奇斗艳。门票只要3元超值。", "view_count": 280, "ratings": [4.6, 4.5]},
    {"user_id": "user_002", "title": "朝阳公园野餐", "location_id": "ATTR_BJ_029", "content": "朝阳公园是北京最大的公园之一。草坪很大，很多人在这儿放风筝、搭帐篷。适合周末休闲。", "view_count": 310, "ratings": [4.4, 4.3]},
]

if __name__ == "__main__":
    import json
    import os
    from datetime import datetime, timedelta
    import random

    data_dir = os.path.dirname(os.path.abspath(__file__))

    # 生成日记数据
    diaries = []
    base_date = datetime(2026, 3, 1)

    for i, d in enumerate(DIARIES):
        # 随机日期
        days_offset = random.randint(0, 24)
        create_date = base_date + timedelta(days=days_offset)

        diaries.append({
            "id": f"diary_{i+1:03d}",
            "user_id": d["user_id"],
            "title": d["title"],
            "content": d["content"],
            "location_id": d["location_id"],
            "images": [],
            "videos": [],
            "view_count": d["view_count"],
            "ratings": d["ratings"],
            "create_time": create_date.strftime("%Y-%m-%d")
        })

    filepath = os.path.join(data_dir, 'diaries.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({"diaries": diaries}, f, ensure_ascii=False, indent=2)

    print(f"日记数据已保存: {len(diaries)} 篇")
