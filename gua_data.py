"""
周易学习程序 - 卦象数据
包含64卦、八卦、以及卦象变换算法
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum


class YaoType(Enum):
    """爻的类型"""

    YANG = 1  # 阳爻 —
    YIN = 0  # 阴爻 - -


@dataclass
class Yao:
    """爻"""

    position: int  # 位置 1-6 (从下往上)
    yao_type: YaoType
    text: str  # 爻辞
    xiang: str  # 象曰

    def flip(self) -> "Yao":
        """翻转阴阳"""
        new_type = YaoType.YIN if self.yao_type == YaoType.YANG else YaoType.YANG
        return Yao(self.position, new_type, self.text, self.xiang)

    @property
    def is_yang(self) -> bool:
        return self.yao_type == YaoType.YANG

    @property
    def symbol(self) -> str:
        return "—" if self.is_yang else "- -"


@dataclass
class Gua:
    """卦"""

    index: int  # 卦序 1-64
    name: str  # 卦名
    chinese_name: str  # 中文名
    description: str  # 卦辞
    xiang: str  # 象曰
    tuan: str  # 彖曰
    yaos: List[Yao]  # 六爻
    upper_gua: str  # 上卦（外卦）
    lower_gua: str  # 下卦（内卦）

    @property
    def binary_code(self) -> str:
        """返回二进制编码，从下往上"""
        return "".join(["1" if y.is_yang else "0" for y in self.yaos])

    @property
    def short_names(self) -> List[str]:
        """返回简称列表，用于搜索"""
        names = [self.name, self.chinese_name]
        # 添加卦象组合名称，如"水天需"
        trigram_names = {
            "qian": "天",
            "kun": "地",
            "zhen": "雷",
            "gen": "山",
            "kan": "水",
            "li": "火",
            "xun": "风",
            "dui": "泽",
        }
        combo = trigram_names.get(self.upper_gua, "") + trigram_names.get(
            self.lower_gua, ""
        )
        if combo:
            names.append(combo + self.name)
            names.append(combo)
        return names

    def get_changed_gua(self, changed_positions: List[int]) -> "Gua":
        """根据变爻位置得到变卦"""
        new_yaos = []
        for yao in self.yaos:
            if yao.position in changed_positions:
                new_yaos.append(yao.flip())
            else:
                new_yaos.append(yao)

        # 创建新卦（临时，需要查找对应的卦）
        binary = "".join(["1" if y.is_yang else "0" for y in new_yaos])
        return binary_to_gua(binary)

    def get_shang_hu_gua(self) -> "Gua":
        """获取上互卦（取345爻为上卦）"""
        # 345爻对应索引 2, 3, 4
        binary = "".join(["1" if self.yaos[i].is_yang else "0" for i in range(2, 5)])
        return binary_to_gua(binary)

    def get_xia_hu_gua(self) -> "Gua":
        """获取下互卦（取234爻为下卦）"""
        # 234爻对应索引 1, 2, 3
        binary = "".join(["1" if self.yaos[i].is_yang else "0" for i in range(1, 4)])
        return binary_to_gua(binary)

    def get_fan_gua(self) -> "Gua":
        """获取反卦（上下卦互换）"""
        lower_binary = "".join(["1" if y.is_yang else "0" for y in self.yaos[:3]])
        upper_binary = "".join(["1" if y.is_yang else "0" for y in self.yaos[3:]])
        binary = upper_binary + lower_binary
        return binary_to_gua(binary)

    def get_dui_gua(self) -> "Gua":
        """获取对卦（错卦，阴阳全反）"""
        binary = "".join(["0" if y.is_yang else "1" for y in self.yaos])
        return binary_to_gua(binary)

    def get_zong_gua(self) -> "Gua":
        """获取综卦（上下颠倒）"""
        binary = "".join(["1" if y.is_yang else "0" for y in reversed(self.yaos)])
        return binary_to_gua(binary)


# 八卦定义
TRIGRAMS = {
    "qian": {
        "name": "乾",
        "symbol": "☰",
        "binary": "111",
        "attribute": "天",
        "nature": "健",
    },
    "kun": {
        "name": "坤",
        "symbol": "☷",
        "binary": "000",
        "attribute": "地",
        "nature": "顺",
    },
    "zhen": {
        "name": "震",
        "symbol": "☳",
        "binary": "100",
        "attribute": "雷",
        "nature": "动",
    },
    "gen": {
        "name": "艮",
        "symbol": "☶",
        "binary": "001",
        "attribute": "山",
        "nature": "止",
    },
    "kan": {
        "name": "坎",
        "symbol": "☵",
        "binary": "010",
        "attribute": "水",
        "nature": "陷",
    },
    "li": {
        "name": "离",
        "symbol": "☲",
        "binary": "101",
        "attribute": "火",
        "nature": "丽",
    },
    "xun": {
        "name": "巽",
        "symbol": "☴",
        "binary": "011",
        "attribute": "风",
        "nature": "入",
    },
    "dui": {
        "name": "兑",
        "symbol": "☱",
        "binary": "110",
        "attribute": "泽",
        "nature": "悦",
    },
}

# 64卦数据
GUA_DATA = [
    # 乾宫
    {
        "index": 1,
        "name": "乾",
        "chinese_name": "乾为天",
        "upper": "qian",
        "lower": "qian",
        "description": "元亨利贞。",
        "xiang": "天行健，君子以自强不息。",
        "tuan": "大哉乾元，万物资始，乃统天。",
        "yaos": [
            {"text": "潜龙勿用。", "xiang": "阳在下也。"},
            {"text": "见龙在田，利见大人。", "xiang": "德施普也。"},
            {"text": "君子终日乾乾，夕惕若，厉无咎。", "xiang": "反复道也。"},
            {"text": "或跃在渊，无咎。", "xiang": "进无咎也。"},
            {"text": "飞龙在天，利见大人。", "xiang": "大人造也。"},
            {"text": "亢龙有悔。", "xiang": "盈不可久也。"},
        ],
    },
    {
        "index": 2,
        "name": "坤",
        "chinese_name": "坤为地",
        "upper": "kun",
        "lower": "kun",
        "description": "元亨，利牝马之贞。",
        "xiang": "地势坤，君子以厚德载物。",
        "tuan": "至哉坤元，万物资生，乃顺承天。",
        "yaos": [
            {"text": "履霜，坚冰至。", "xiang": "驯致其道，至坚冰也。"},
            {"text": "直方大，不习无不利。", "xiang": "地道光也。"},
            {"text": "含章可贞。或从王事，无成有终。", "xiang": "知光大也。"},
            {"text": "括囊，无咎无誉。", "xiang": "慎不害也。"},
            {"text": "黄裳，元吉。", "xiang": "文在中也。"},
            {"text": "龙战于野，其血玄黄。", "xiang": "其道穷也。"},
        ],
    },
    {
        "index": 3,
        "name": "屯",
        "chinese_name": "水雷屯",
        "upper": "kan",
        "lower": "zhen",
        "description": "元亨利贞，勿用，有攸往，利建侯。",
        "xiang": "云雷屯，君子以经纶。",
        "tuan": "屯，刚柔始交而难生，动乎险中。",
        "yaos": [
            {"text": "磐桓，利居贞，利建侯。", "xiang": "虽磐桓，志行正也。"},
            {
                "text": "屯如邅如，乘马班如。匪寇婚媾，女子贞不字，十年乃字。",
                "xiang": "六二之难，乘刚也。",
            },
            {
                "text": "即鹿无虞，惟入于林中。君子几不如舍，往吝。",
                "xiang": "即鹿无虞，以从禽也。",
            },
            {"text": "乘马班如，求婚媾，往吉，无不利。", "xiang": "求而往，明也。"},
            {"text": "屯其膏，小贞吉，大贞凶。", "xiang": "屯其膏，施未光也。"},
            {"text": "乘马班如，泣血涟如。", "xiang": "泣血涟如，何可长也。"},
        ],
    },
    {
        "index": 4,
        "name": "蒙",
        "chinese_name": "山水蒙",
        "upper": "gen",
        "lower": "kan",
        "description": "亨。匪我求童蒙，童蒙求我。",
        "xiang": "山下出泉，蒙。君子以果行育德。",
        "tuan": "蒙，山下有险，险而止，蒙。",
        "yaos": [
            {
                "text": "发蒙，利用刑人，用说桎梏，以往吝。",
                "xiang": "利用刑人，以正法也。",
            },
            {"text": "包蒙吉，纳妇吉，子克家。", "xiang": "子克家，刚柔接也。"},
            {
                "text": "勿用取女，见金夫，不有躬，无攸利。",
                "xiang": "勿用取女，行不顺也。",
            },
            {"text": "困蒙，吝。", "xiang": "困蒙之吝，独远实也。"},
            {"text": "童蒙，吉。", "xiang": "童蒙之吉，顺以巽也。"},
            {"text": "击蒙，不利为寇，利御寇。", "xiang": "利用御寇，上下顺也。"},
        ],
    },
    {
        "index": 5,
        "name": "需",
        "chinese_name": "水天需",
        "upper": "kan",
        "lower": "qian",
        "description": "有孚，光亨，贞吉。利涉大川。",
        "xiang": "云上于天，需。君子以饮食宴乐。",
        "tuan": "需，须也，险在前也。",
        "yaos": [
            {"text": "需于郊，利用恒，无咎。", "xiang": "需于郊，不犯难行也。"},
            {"text": "需于沙，小有言，终吉。", "xiang": "需于沙，衍在中也。"},
            {"text": "需于泥，致寇至。", "xiang": "需于泥，灾在外也。"},
            {"text": "需于血，出自穴。", "xiang": "需于血，顺以听也。"},
            {"text": "需于酒食，贞吉。", "xiang": "酒食贞吉，以中正也。"},
            {
                "text": "入于穴，有不速之客三人来，敬之终吉。",
                "xiang": "不速之客来，敬之终吉。",
            },
        ],
    },
    {
        "index": 6,
        "name": "讼",
        "chinese_name": "天水讼",
        "upper": "qian",
        "lower": "kan",
        "description": "有孚，窒惕，中吉，终凶。",
        "xiang": "天与水违行，讼。君子以作事谋始。",
        "tuan": "讼，上刚下险，险而健，讼。",
        "yaos": [
            {"text": "不永所事，小有言，终吉。", "xiang": "不永所事，讼不可长也。"},
            {
                "text": "不克讼，归而逋，其邑人三百户，无眚。",
                "xiang": "不克讼，归逋窜也。",
            },
            {
                "text": "食旧德，贞厉，终吉。或从王事，无成。",
                "xiang": "食旧德，从上吉也。",
            },
            {"text": "不克讼，复即命渝，安贞吉。", "xiang": "复即命渝，安贞不失也。"},
            {"text": "讼元吉。", "xiang": "讼元吉，以中正也。"},
            {"text": "或锡之鞶带，终朝三褫之。", "xiang": "以讼受服，亦不足敬也。"},
        ],
    },
    {
        "index": 7,
        "name": "师",
        "chinese_name": "地水师",
        "upper": "kun",
        "lower": "kan",
        "description": "贞，丈人吉，无咎。",
        "xiang": "地中有水，师。君子以容民畜众。",
        "tuan": "师，众也，贞，正也。",
        "yaos": [
            {"text": "师出以律，否臧凶。", "xiang": "师出以律，失律凶也。"},
            {"text": "在师中，吉无咎，王三锡命。", "xiang": "在师中吉，承天宠也。"},
            {"text": "师或舆尸，凶。", "xiang": "师或舆尸，大无功也。"},
            {"text": "师左次，无咎。", "xiang": "左次无咎，未失常也。"},
            {
                "text": "田有禽，利执言，无咎。长子帅师，弟子舆尸，贞凶。",
                "xiang": "长子帅师，以中行也。",
            },
            {"text": "大君有命，开国承家，小人勿用。", "xiang": "大君有命，以正功也。"},
        ],
    },
    {
        "index": 8,
        "name": "比",
        "chinese_name": "水地比",
        "upper": "kan",
        "lower": "kun",
        "description": "吉。原筮元永贞，无咎。不宁方来，后夫凶。",
        "xiang": "地上有水，比。先王以建万国，亲诸侯。",
        "tuan": "比，吉也。比，辅也，下顺从也。",
        "yaos": [
            {
                "text": "有孚比之，无咎。有孚盈缶，终来有它，吉。",
                "xiang": "比之初六，有它吉也。",
            },
            {"text": "比之自内，贞吉。", "xiang": "比之自内，不自失也。"},
            {"text": "比之匪人。", "xiang": "比之匪人，不亦伤乎！"},
            {"text": "外比之，贞吉。", "xiang": "外比于贤，以从上也。"},
            {
                "text": "显比，王用三驱，失前禽。邑人不诫，吉。",
                "xiang": "显比之吉，位正中也。",
            },
            {"text": "比之无首，凶。", "xiang": "比之无首，无所终也。"},
        ],
    },
    # 更多卦象数据...
    # 这里只列出前8卦作为示例，完整版本需要添加所有64卦
]


# 尝试导入完整数据
try:
    from yijing_full_data import YIJING_DATA

    HAS_FULL_DATA = True
except ImportError:
    HAS_FULL_DATA = False
    YIJING_DATA = {}


# 初始化完整的64卦数据
def init_gua_data() -> List[Gua]:
    """初始化所有64卦数据"""
    gua_list = []

    # 完整的64卦二进制编码（从下到上）
    # 格式: (二进制编码, 卦名, 中文名, 上卦, 下卦)
    # 二进制编码 = 下卦编码 + 上卦编码
    gua_patterns = [
        ("111111", "乾", "乾为天", "qian", "qian"),
        ("000000", "坤", "坤为地", "kun", "kun"),
        ("100010", "屯", "水雷屯", "kan", "zhen"),
        ("010001", "蒙", "山水蒙", "gen", "kan"),
        ("111010", "需", "水天需", "kan", "qian"),
        ("010111", "讼", "天水讼", "qian", "kan"),
        ("010000", "师", "地水师", "kun", "kan"),
        ("000010", "比", "水地比", "kan", "kun"),
        ("111011", "小畜", "风天小畜", "xun", "qian"),
        ("110111", "履", "天泽履", "qian", "dui"),
        ("111000", "泰", "地天泰", "kun", "qian"),
        ("000111", "否", "天地否", "qian", "kun"),
        ("101111", "同人", "天火同人", "qian", "li"),
        ("111101", "大有", "火天大有", "li", "qian"),
        ("001000", "谦", "地山谦", "kun", "gen"),
        ("000100", "豫", "雷地豫", "zhen", "kun"),
        ("100110", "随", "泽雷随", "dui", "zhen"),
        ("011001", "蛊", "山风蛊", "gen", "xun"),
        ("110000", "临", "地泽临", "kun", "dui"),
        ("000011", "观", "风地观", "xun", "kun"),
        ("100101", "噬嗑", "火雷噬嗑", "li", "zhen"),
        ("101001", "贲", "山火贲", "gen", "li"),
        ("000001", "剥", "山地剥", "gen", "kun"),
        ("100000", "复", "地雷复", "kun", "zhen"),
        ("100111", "无妄", "天雷无妄", "qian", "zhen"),
        ("111001", "大畜", "山天大畜", "gen", "qian"),
        ("100001", "颐", "山雷颐", "gen", "zhen"),
        ("011110", "大过", "泽风大过", "dui", "xun"),
        ("010010", "坎", "坎为水", "kan", "kan"),
        ("101101", "离", "离为火", "li", "li"),
        ("001110", "咸", "泽山咸", "dui", "gen"),
        ("011100", "恒", "雷风恒", "zhen", "xun"),
        ("001111", "遁", "天山遁", "qian", "gen"),
        ("111100", "大壮", "雷天大壮", "zhen", "qian"),
        ("000101", "晋", "火地晋", "li", "kun"),
        ("101000", "明夷", "地火明夷", "kun", "li"),
        ("101011", "家人", "风火家人", "xun", "li"),
        ("110101", "睽", "火泽睽", "li", "dui"),
        ("001010", "蹇", "水山蹇", "kan", "gen"),
        ("010100", "解", "雷水解", "zhen", "kan"),
        ("110001", "损", "山泽损", "gen", "dui"),
        ("100011", "益", "风雷益", "xun", "zhen"),
        ("111110", "夬", "泽天夬", "dui", "qian"),
        ("011111", "姤", "天风姤", "qian", "xun"),
        ("000110", "萃", "泽地萃", "dui", "kun"),
        ("011000", "升", "地风升", "kun", "xun"),
        ("010110", "困", "泽水困", "dui", "kan"),
        ("011010", "井", "水风井", "kan", "xun"),
        ("101110", "革", "泽火革", "dui", "li"),
        ("011101", "鼎", "火风鼎", "li", "xun"),
        ("100100", "震", "震为雷", "zhen", "zhen"),
        ("001001", "艮", "艮为山", "gen", "gen"),
        ("001011", "渐", "风山渐", "xun", "gen"),
        ("110100", "归妹", "雷泽归妹", "zhen", "dui"),
        ("101100", "丰", "雷火丰", "zhen", "li"),
        ("001101", "旅", "火山旅", "li", "gen"),
        ("011011", "巽", "巽为风", "xun", "xun"),
        ("110110", "兑", "兑为泽", "dui", "dui"),
        ("010011", "涣", "风水涣", "xun", "kan"),
        ("110010", "节", "水泽节", "kan", "dui"),
        ("110011", "中孚", "风泽中孚", "xun", "dui"),
        ("001100", "小过", "雷山小过", "zhen", "gen"),
        ("101010", "既济", "水火既济", "kan", "li"),
        ("010101", "未济", "火水未济", "li", "kan"),
    ]

    # 使用 GUA_DATA 或 YIJING_DATA 中的真实数据
    for i, (binary, name, chinese_name, upper, lower) in enumerate(gua_patterns, 1):
        # 优先从 YIJING_DATA 获取完整数据
        gua_data = None
        if HAS_FULL_DATA and name in YIJING_DATA:
            gua_data = YIJING_DATA[name]
        else:
            # 从 GUA_DATA 查找
            for gd in GUA_DATA:
                if gd["index"] == i:
                    gua_data = gd
                    break

        # 如果没找到，使用默认值
        if gua_data is None:
            gua_data = {
                "description": f"{name}卦辞",
                "xiang": f"{name}之象",
                "tuan": f"{name}之彖",
                "yaos": [
                    {"text": f"{name}第{pos + 1}爻", "xiang": ""} for pos in range(6)
                ],
            }

        yaos = []
        for pos in range(6):
            is_yang = binary[pos] == "1"
            yao_type = YaoType.YANG if is_yang else YaoType.YIN

            # 获取爻辞（注意：GUA_DATA中的爻辞是从初爻到上爻，pos=0是初爻）
            yao_text = gua_data["yaos"][pos]["text"]
            yao_xiang = gua_data["yaos"][pos]["xiang"]

            yaos.append(
                Yao(
                    position=pos + 1,
                    yao_type=yao_type,
                    text=yao_text,
                    xiang=yao_xiang,
                )
            )

        gua = Gua(
            index=i,
            name=name,
            chinese_name=chinese_name,
            description=gua_data["description"],
            xiang=gua_data["xiang"],
            tuan=gua_data["tuan"],
            yaos=yaos,
            upper_gua=upper,
            lower_gua=lower,
        )
        gua_list.append(gua)

    return gua_list


# 全局卦象数据
ALL_GUAS: List[Gua] = []
GUA_MAP: Dict[str, Gua] = {}  # 二进制编码到卦的映射


def init_data():
    """初始化数据"""
    global ALL_GUAS, GUA_MAP
    ALL_GUAS = init_gua_data()
    GUA_MAP = {gua.binary_code: gua for gua in ALL_GUAS}


def binary_to_gua(binary: str) -> Gua:
    """根据二进制编码获取卦"""
    if not GUA_MAP:
        init_data()
    return GUA_MAP.get(binary, ALL_GUAS[0])


def search_gua(query: str) -> List[Gua]:
    """搜索卦象"""
    if not ALL_GUAS:
        init_data()

    query = query.lower().strip()
    results = []

    for gua in ALL_GUAS:
        # 搜索卦名
        if query in gua.name or query in gua.chinese_name:
            results.append(gua)
            continue

        # 搜索简称（如"水天"）
        for short_name in gua.short_names:
            if query in short_name:
                results.append(gua)
                break

    return results


def get_gua_by_index(index: int) -> Optional[Gua]:
    """根据序号获取卦"""
    if not ALL_GUAS:
        init_data()
    if 1 <= index <= 64:
        return ALL_GUAS[index - 1]
    return None


# 初始化
init_data()
