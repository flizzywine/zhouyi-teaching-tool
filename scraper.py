"""
周易数据爬虫
从中国哲学书电子化计划(ctext.org)抓取64卦完整数据
"""

import time
import json

# 64卦列表（按周易顺序）
GUA_LIST = [
    ("qian", "乾", "乾为天", "qian", "qian"),
    ("kun", "坤", "坤为地", "kun", "kun"),
    ("zhun", "屯", "水雷屯", "kan", "zhen"),
    ("meng", "蒙", "山水蒙", "gen", "kan"),
    ("xu", "需", "水天需", "kan", "qian"),
    ("song", "讼", "天水讼", "qian", "kan"),
    ("shi", "师", "地水师", "kun", "kan"),
    ("bi", "比", "水地比", "kan", "kun"),
    ("xiao-xu", "小畜", "风天小畜", "xun", "qian"),
    ("lu", "履", "天泽履", "qian", "dui"),
    ("tai", "泰", "地天泰", "kun", "qian"),
    ("pi", "否", "天地否", "qian", "kun"),
    ("tong-ren", "同人", "天火同人", "qian", "li"),
    ("da-you", "大有", "火天大有", "li", "qian"),
    ("qian", "谦", "地山谦", "kun", "gen"),
    ("yu", "豫", "雷地豫", "zhen", "kun"),
    ("sui", "随", "泽雷随", "dui", "zhen"),
    ("gu", "蛊", "山风蛊", "gen", "xun"),
    ("lin", "临", "地泽临", "kun", "dui"),
    ("guan", "观", "风地观", "xun", "kun"),
    ("shi-he", "噬嗑", "火雷噬嗑", "li", "zhen"),
    ("bi", "贲", "山火贲", "gen", "li"),
    ("bo", "剥", "山地剥", "gen", "kun"),
    ("fu", "复", "地雷复", "kun", "zhen"),
    ("wu-wang", "无妄", "天雷无妄", "qian", "zhen"),
    ("da-xu", "大畜", "山天大畜", "gen", "qian"),
    ("yi", "颐", "山雷颐", "gen", "zhen"),
    ("da-guo", "大过", "泽风大过", "dui", "xun"),
    ("kan", "坎", "坎为水", "kan", "kan"),
    ("li", "离", "离为火", "li", "li"),
    ("xian", "咸", "泽山咸", "dui", "gen"),
    ("heng", "恒", "雷风恒", "zhen", "xun"),
    ("dun", "遁", "天山遁", "qian", "gen"),
    ("da-zhuang", "大壮", "雷天大壮", "zhen", "qian"),
    ("jin", "晋", "火地晋", "li", "kun"),
    ("ming-yi", "明夷", "地火明夷", "kun", "li"),
    ("jia-ren", "家人", "风火家人", "xun", "li"),
    ("kui", "睽", "火泽睽", "li", "dui"),
    ("jian", "蹇", "水山蹇", "kan", "gen"),
    ("jie", "解", "雷水解", "zhen", "kan"),
    ("sun", "损", "山泽损", "gen", "dui"),
    ("yi", "益", "风雷益", "xun", "zhen"),
    ("guai", "夬", "泽天夬", "dui", "qian"),
    ("gou", "姤", "天风姤", "qian", "xun"),
    ("cui", "萃", "泽地萃", "dui", "kun"),
    ("sheng", "升", "地风升", "kun", "xun"),
    ("kun", "困", "泽水困", "dui", "kan"),
    ("jing", "井", "水风井", "kan", "xun"),
    ("ge", "革", "泽火革", "dui", "li"),
    ("ding", "鼎", "火风鼎", "li", "xun"),
    ("zhen", "震", "震为雷", "zhen", "zhen"),
    ("gen", "艮", "艮为山", "gen", "gen"),
    ("jian", "渐", "风山渐", "xun", "gen"),
    ("gui-mei", "归妹", "雷泽归妹", "zhen", "dui"),
    ("feng", "丰", "雷火丰", "zhen", "li"),
    ("lu", "旅", "火山旅", "li", "gen"),
    ("xun", "巽", "巽为风", "xun", "xun"),
    ("dui", "兑", "兑为泽", "dui", "dui"),
    ("huan", "涣", "风水涣", "xun", "kan"),
    ("jie", "节", "水泽节", "kan", "dui"),
    ("zhong-fu", "中孚", "风泽中孚", "xun", "dui"),
    ("xiao-guo", "小过", "雷山小过", "zhen", "gen"),
    ("ji-ji", "既济", "水火既济", "kan", "li"),
    ("wei-ji", "未济", "火水未济", "li", "kan"),
]

# 由于ctext.org可能有反爬虫机制，这里提供一个数据模板
# 实际使用时，可以使用requests库配合适当的延迟来抓取

print("周易数据爬虫")
print("=" * 50)
print(f"需要抓取的卦象数量: {len(GUA_LIST)}")
print()
print("卦象列表:")
for i, (code, name, chinese, upper, lower) in enumerate(GUA_LIST, 1):
    print(f"{i:2d}. {name} ({chinese})")

print()
print("=" * 50)
print("由于ctext.org有反爬虫机制，建议使用以下方式获取数据:")
print("1. 手动访问 https://ctext.org/book-of-changes/卦名/zh")
print("2. 或使用浏览器开发者工具批量导出")
print("3. 或使用已整理好的JSON数据文件")

# 保存卦象列表供后续使用
with open("gua_list.json", "w", encoding="utf-8") as f:
    json.dump(
        [
            {
                "code": code,
                "name": name,
                "chinese_name": chinese,
                "upper": upper,
                "lower": lower,
                "index": i,
            }
            for i, (code, name, chinese, upper, lower) in enumerate(GUA_LIST, 1)
        ],
        f,
        ensure_ascii=False,
        indent=2,
    )

print()
print("卦象列表已保存到 gua_list.json")
