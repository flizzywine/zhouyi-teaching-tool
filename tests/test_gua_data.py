"""
测试 gua_data.py 核心数据结构和算法
"""

import pytest
from gua_data import Yao, Gua, YaoType, binary_to_gua, search_gua, get_gua_by_index


class TestYao:
    """测试爻类"""

    def test_yang_yao_creation(self):
        """测试阳爻创建"""
        yao = Yao(position=1, yao_type=YaoType.YANG, text="测试", xiang="象曰")
        assert yao.position == 1
        assert yao.yao_type == YaoType.YANG
        assert yao.is_yang == True
        assert yao.symbol == "—"
        assert yao.text == "测试"
        assert yao.xiang == "象曰"

    def test_yin_yao_creation(self):
        """测试阴爻创建"""
        yao = Yao(position=2, yao_type=YaoType.YIN, text="测试", xiang="象曰")
        assert yao.position == 2
        assert yao.yao_type == YaoType.YIN
        assert yao.is_yang == False
        assert yao.symbol == "- -"

    def test_yao_flip_yang_to_yin(self):
        """测试阳爻翻转为阴爻"""
        yang_yao = Yao(position=1, yao_type=YaoType.YANG, text="测试", xiang="象曰")
        yin_yao = yang_yao.flip()
        assert yin_yao.yao_type == YaoType.YIN
        assert yin_yao.position == yang_yao.position
        assert yin_yao.text == yang_yao.text

    def test_yao_flip_yin_to_yang(self):
        """测试阴爻翻转为阳爻"""
        yin_yao = Yao(position=1, yao_type=YaoType.YIN, text="测试", xiang="象曰")
        yang_yao = yin_yao.flip()
        assert yang_yao.yao_type == YaoType.YANG


class TestGua:
    """测试卦类"""

    def test_gua_creation(self, sample_gua_qian):
        """测试卦创建"""
        gua = sample_gua_qian
        assert gua.index == 1
        assert gua.name == "乾"
        assert gua.chinese_name == "乾为天"
        assert len(gua.yaos) == 6
        assert gua.upper_gua == "qian"
        assert gua.lower_gua == "qian"

    def test_binary_code(self, sample_gua_qian, sample_gua_kun):
        """测试二进制编码"""
        assert sample_gua_qian.binary_code == "111111"
        assert sample_gua_kun.binary_code == "000000"

    def test_short_names(self, sample_gua_qian):
        """测试简称列表"""
        short_names = sample_gua_qian.short_names
        assert "乾" in short_names
        assert "乾为天" in short_names
        assert "天天乾" in short_names
        assert "天天" in short_names


class TestBinaryToGua:
    """测试二进制编码转卦函数"""

    def test_binary_to_gua_qian(self):
        """测试乾卦二进制编码"""
        gua = binary_to_gua("111111")
        assert gua.name == "乾"

    def test_binary_to_gua_kun(self):
        """测试坤卦二进制编码"""
        gua = binary_to_gua("000000")
        assert gua.name == "坤"

    def test_binary_to_gua_invalid(self):
        """测试无效二进制编码返回默认卦"""
        gua = binary_to_gua("invalid")
        # 无效编码返回第一个卦（乾卦）
        assert gua.name == "乾"

    @pytest.mark.parametrize(
        "binary,expected_name",
        [
            ("111111", "乾"),
            ("000000", "坤"),
            ("100010", "屯"),
            ("010001", "蒙"),
            ("111010", "需"),
            ("010111", "讼"),
            ("010000", "师"),
            ("000010", "比"),
        ],
    )
    def test_binary_to_gua_parametrized(self, binary, expected_name):
        """参数化测试二进制编码"""
        gua = binary_to_gua(binary)
        assert gua.name == expected_name


class TestSearchGua:
    """测试搜索功能"""

    def test_search_by_name(self):
        """测试按卦名搜索"""
        results = search_gua("乾")
        assert len(results) >= 1
        assert any(g.name == "乾" for g in results)

    def test_search_by_chinese_name(self):
        """测试按中文名搜索"""
        results = search_gua("乾为天")
        assert len(results) >= 1
        assert any(g.chinese_name == "乾为天" for g in results)

    def test_search_by_short_name(self):
        """测试按简称搜索"""
        results = search_gua("水天")
        assert len(results) >= 1
        # 水天需卦
        assert any("需" in g.name for g in results)

    def test_search_no_results(self):
        """测试无结果搜索"""
        results = search_gua("不存在的卦")
        assert len(results) == 0

    def test_search_case_insensitive(self):
        """测试搜索不区分大小写"""
        results_lower = search_gua("qian")
        results_upper = search_gua("QIAN")
        # 搜索结果应该相同
        assert len(results_lower) == len(results_upper)


class TestGetGuaByIndex:
    """测试按索引获取卦"""

    def test_get_gua_valid_index(self):
        """测试有效索引"""
        gua = get_gua_by_index(1)
        assert gua is not None
        assert gua.name == "乾"

    def test_get_gua_index_64(self):
        """测试第64卦"""
        gua = get_gua_by_index(64)
        assert gua is not None
        assert gua.index == 64

    def test_get_gua_invalid_index_zero(self):
        """测试无效索引0"""
        gua = get_gua_by_index(0)
        assert gua is None

    def test_get_gua_invalid_index_too_large(self):
        """测试超出范围的索引"""
        gua = get_gua_by_index(65)
        assert gua is None

    def test_get_gua_negative_index(self):
        """测试负索引"""
        gua = get_gua_by_index(-1)
        assert gua is None
