"""
测试64卦数据完整性
验证所有卦象数据是否完整、正确
"""

import pytest
from gua_data import ALL_GUAS, YIJING_DATA, HAS_FULL_DATA


class TestGuaDataCompleteness:
    """测试卦象数据完整性"""

    def test_all_64_guas_exist(self, gua_data):
        """测试是否存在64个卦"""
        assert len(gua_data["all_guas"]) == 64, (
            f"应该有64个卦，实际有{len(gua_data['all_guas'])}个"
        )

    def test_all_indices_unique(self, gua_data):
        """测试所有卦索引唯一"""
        indices = [gua.index for gua in gua_data["all_guas"]]
        assert len(indices) == len(set(indices)), "卦索引不唯一"
        assert set(indices) == set(range(1, 65)), "卦索引应该为1-64"

    def test_all_binary_codes_unique(self, gua_data):
        """测试所有二进制编码唯一"""
        codes = [gua.binary_code for gua in gua_data["all_guas"]]
        assert len(codes) == len(set(codes)), "二进制编码不唯一"

    def test_all_binary_codes_valid(self, gua_data):
        """测试所有二进制编码有效"""
        for gua in gua_data["all_guas"]:
            assert len(gua.binary_code) == 6, f"{gua.name}的二进制编码长度不是6"
            assert set(gua.binary_code).issubset({"0", "1"}), (
                f"{gua.name}的二进制编码包含无效字符"
            )

    def test_all_names_not_empty(self, gua_data):
        """测试所有卦名不为空"""
        for gua in gua_data["all_guas"]:
            assert gua.name, f"索引{gua.index}的卦名为空"
            assert gua.chinese_name, f"{gua.name}的中文名为空"

    def test_all_descriptions_not_empty(self, gua_data):
        """测试所有卦辞不为空"""
        for gua in gua_data["all_guas"]:
            assert gua.description, f"{gua.name}的卦辞为空"

    def test_all_have_six_yaos(self, gua_data):
        """测试所有卦都有6个爻"""
        for gua in gua_data["all_guas"]:
            assert len(gua.yaos) == 6, f"{gua.name}应该有6个爻，实际有{len(gua.yaos)}个"

    def test_yao_positions_correct(self, gua_data):
        """测试爻位置正确（1-6）"""
        for gua in gua_data["all_guas"]:
            positions = [yao.position for yao in gua.yaos]
            assert set(positions) == {1, 2, 3, 4, 5, 6}, f"{gua.name}的爻位置不正确"

    def test_all_yaos_have_text(self, gua_data):
        """测试所有爻都有爻辞"""
        for gua in gua_data["all_guas"]:
            for yao in gua.yaos:
                assert yao.text, f"{gua.name}第{yao.position}爻的爻辞为空"

    def test_trigrams_valid(self, gua_data):
        """测试上下卦属性有效"""
        valid_trigrams = {"qian", "kun", "zhen", "gen", "kan", "li", "xun", "dui"}
        for gua in gua_data["all_guas"]:
            assert gua.upper_gua in valid_trigrams, (
                f"{gua.name}的上卦{gua.upper_gua}无效"
            )
            assert gua.lower_gua in valid_trigrams, (
                f"{gua.name}的下卦{gua.lower_gua}无效"
            )


class TestYijingFullData:
    """测试完整数据文件"""

    def test_full_data_loaded(self):
        """测试完整数据是否加载"""
        # 注意：如果yijing_full_data.py不存在，此测试会被跳过
        if not HAS_FULL_DATA:
            pytest.skip("完整数据文件未找到")

    def test_full_data_has_all_guas(self):
        """测试完整数据包含所有64卦"""
        if not HAS_FULL_DATA:
            pytest.skip("完整数据文件未找到")
        assert len(YIJING_DATA) == 64, (
            f"完整数据应该有64个卦，实际有{len(YIJING_DATA)}个"
        )

    def test_full_data_structure(self):
        """测试完整数据结构正确"""
        if not HAS_FULL_DATA:
            pytest.skip("完整数据文件未找到")

        required_fields = {
            "index",
            "chinese_name",
            "upper",
            "lower",
            "description",
            "tuan",
            "xiang",
            "yaos",
        }
        for name, data in YIJING_DATA.items():
            missing = required_fields - set(data.keys())
            assert not missing, f"{name}缺少字段: {missing}"

            # 检查yaos
            assert len(data["yaos"]) == 6, f"{name}应该有6个爻"
            for i, yao in enumerate(data["yaos"]):
                assert "text" in yao, f"{name}第{i + 1}爻缺少text"
                assert "xiang" in yao, f"{name}第{i + 1}爻缺少xiang"


class TestSpecificGuas:
    """测试特定卦的数据正确性"""

    def test_qian_gua_data(self, gua_data):
        """测试乾卦数据"""
        qian = gua_data["gua_map"]["111111"]
        assert qian.name == "乾"
        assert qian.chinese_name == "乾为天"
        assert qian.upper_gua == "qian"
        assert qian.lower_gua == "qian"
        assert len(qian.yaos) == 6
        # 乾卦六爻皆阳
        assert all(yao.is_yang for yao in qian.yaos)

    def test_kun_gua_data(self, gua_data):
        """测试坤卦数据"""
        kun = gua_data["gua_map"]["000000"]
        assert kun.name == "坤"
        assert kun.chinese_name == "坤为地"
        assert kun.upper_gua == "kun"
        assert kun.lower_gua == "kun"
        # 坤卦六爻皆阴
        assert all(not yao.is_yang for yao in kun.yaos)

    def test_tai_gua_data(self, gua_data):
        """测试泰卦数据（地天泰）"""
        tai = gua_data["gua_map"]["111000"]
        assert tai.name == "泰"
        assert tai.chinese_name == "地天泰"
        assert tai.upper_gua == "kun"  # 上卦为地
        assert tai.lower_gua == "qian"  # 下卦为天

    def test_pi_gua_data(self, gua_data):
        """测试否卦数据（天地否）"""
        pi = gua_data["gua_map"]["000111"]
        assert pi.name == "否"
        assert pi.chinese_name == "天地否"
        assert pi.upper_gua == "qian"  # 上卦为天
        assert pi.lower_gua == "kun"  # 下卦为地


class TestDataConsistency:
    """测试数据一致性"""

    def test_binary_matches_trigrams(self, gua_data):
        """测试二进制编码与上下卦一致"""
        trigram_binary = {
            "qian": "111",
            "kun": "000",
            "zhen": "100",
            "gen": "001",
            "kan": "010",
            "li": "101",
            "xun": "011",
            "dui": "110",
        }

        for gua in gua_data["all_guas"]:
            # 二进制编码 = 下卦 + 上卦（从下到上）
            expected_lower = trigram_binary[gua.lower_gua]
            expected_upper = trigram_binary[gua.upper_gua]
            expected = expected_lower + expected_upper

            assert gua.binary_code == expected, (
                f"{gua.name}的二进制编码{gua.binary_code}与上下卦不匹配，期望{expected}"
            )
