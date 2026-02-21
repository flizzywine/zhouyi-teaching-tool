"""
测试卦象变换算法（错卦、综卦、反卦、互卦、变卦）
"""

import pytest
from gua_data import binary_to_gua


class TestDuiGua:
    """测试错卦（对卦，阴阳全反）"""

    def test_qian_dui_gua_is_kun(self, gua_data):
        """测试乾卦的错卦是坤卦"""
        qian = gua_data["gua_map"]["111111"]
        dui = qian.get_dui_gua()
        assert dui.name == "坤"
        assert dui.binary_code == "000000"

    def test_kun_dui_gua_is_qian(self, gua_data):
        """测试坤卦的错卦是乾卦"""
        kun = gua_data["gua_map"]["000000"]
        dui = kun.get_dui_gua()
        assert dui.name == "乾"
        assert dui.binary_code == "111111"

    def test_dui_gua_involution(self, gua_data):
        """测试错卦的错卦回到原卦（对合性）"""
        for gua in gua_data["all_guas"]:
            dui = gua.get_dui_gua()
            dui_dui = dui.get_dui_gua()
            assert dui_dui.binary_code == gua.binary_code, (
                f"{gua.name}的错卦的错卦应该是自身"
            )

    @pytest.mark.parametrize(
        "binary,expected_dui",
        [
            ("111111", "000000"),  # 乾 -> 坤
            ("000000", "111111"),  # 坤 -> 乾
            ("100010", "011101"),  # 屯 -> 鼎
            ("010001", "101110"),  # 蒙 -> 革
        ],
    )
    def test_dui_gua_parametrized(self, gua_data, binary, expected_dui):
        """参数化测试错卦"""
        gua = gua_data["gua_map"][binary]
        dui = gua.get_dui_gua()
        assert dui.binary_code == expected_dui


class TestZongGua:
    """测试综卦（上下颠倒）"""

    def test_qian_zong_gua_is_qian(self, gua_data):
        """测试乾卦的综卦是自身（对称）"""
        qian = gua_data["gua_map"]["111111"]
        zong = qian.get_zong_gua()
        assert zong.binary_code == "111111"

    def test_kun_zong_gua_is_kun(self, gua_data):
        """测试坤卦的综卦是自身（对称）"""
        kun = gua_data["gua_map"]["000000"]
        zong = kun.get_zong_gua()
        assert zong.binary_code == "000000"

    def test_zong_gua_involution(self, gua_data):
        """测试综卦的综卦回到原卦（对合性）"""
        for gua in gua_data["all_guas"]:
            zong = gua.get_zong_gua()
            zong_zong = zong.get_zong_gua()
            assert zong_zong.binary_code == gua.binary_code, (
                f"{gua.name}的综卦的综卦应该是自身"
            )

    def test_tai_pi_zong_gua(self, gua_data):
        """测试泰卦和否卦互为综卦"""
        tai = gua_data["gua_map"]["111000"]  # 地天泰
        pi = gua_data["gua_map"]["000111"]  # 天地否

        assert tai.get_zong_gua().binary_code == pi.binary_code
        assert pi.get_zong_gua().binary_code == tai.binary_code


class TestFanGua:
    """测试反卦（上下卦互换）"""

    def test_fan_gua_swaps_trigrams(self, gua_data):
        """测试反卦交换上下卦"""
        tai = gua_data["gua_map"]["111000"]  # 地天泰（上地下天）
        fan = tai.get_fan_gua()
        # 反卦应该是天地否（上天下地）
        assert fan.binary_code == "000111"
        assert fan.name == "否"

    def test_fan_gua_involution(self, gua_data):
        """测试反卦的反卦回到原卦（对合性）"""
        for gua in gua_data["all_guas"]:
            fan = gua.get_fan_gua()
            fan_fan = fan.get_fan_gua()
            assert fan_fan.binary_code == gua.binary_code, (
                f"{gua.name}的反卦的反卦应该是自身"
            )


class TestHuGua:
    """测试互卦"""

    def test_shang_hu_gua_extraction(self, gua_data):
        """测试上互卦提取（345爻）"""
        # 以乾卦为例，345爻都是阳，应该得到乾卦
        qian = gua_data["gua_map"]["111111"]
        shang_hu = qian.get_shang_hu_gua()
        # 345爻 = 111 = 乾卦(111111)
        assert shang_hu.name == "乾"

    def test_xia_hu_gua_extraction(self, gua_data):
        """测试下互卦提取（234爻）"""
        qian = gua_data["gua_map"]["111111"]
        xia_hu = qian.get_xia_hu_gua()
        # 234爻 = 111 = 乾卦
        assert xia_hu.name == "乾"

    def test_hu_gua_returns_valid_gua(self, gua_data):
        """测试互卦返回有效的卦"""
        for gua in gua_data["all_guas"]:
            shang_hu = gua.get_shang_hu_gua()
            xia_hu = gua.get_xia_hu_gua()
            assert shang_hu is not None, f"{gua.name}的上互卦为None"
            assert xia_hu is not None, f"{gua.name}的下互卦为None"
            # 互卦返回的是64卦之一
            assert shang_hu.binary_code in gua_data["gua_map"], (
                f"{gua.name}的上互卦无效"
            )
            assert xia_hu.binary_code in gua_data["gua_map"], f"{gua.name}的下互卦无效"


class TestChangedGua:
    """测试变卦（爻翻转）"""

    def test_change_single_yao(self, gua_data):
        """测试单爻变化"""
        qian = gua_data["gua_map"]["111111"]  # 乾卦
        # 变第1爻（初爻）
        changed = qian.get_changed_gua([1])
        # yaos列表顺序是[1,2,3,4,5,6]，binary_code按此顺序
        # 变第1爻会改变binary_code[0]，得到011111
        assert changed.binary_code == "011111"

    def test_change_multiple_yaos(self, gua_data):
        """测试多爻变化"""
        qian = gua_data["gua_map"]["111111"]
        # 变第1、2、3爻
        changed = qian.get_changed_gua([1, 2, 3])
        # 变第1,2,3爻会改变binary_code[0],[1],[2]，得到000111
        assert changed.binary_code == "000111"

    def test_change_all_yaos(self, gua_data):
        """测试六爻全变"""
        qian = gua_data["gua_map"]["111111"]
        changed = qian.get_changed_gua([1, 2, 3, 4, 5, 6])
        # 六爻全变应该得到坤卦
        assert changed.binary_code == "000000"
        assert changed.name == "坤"

    def test_change_no_yaos(self, gua_data):
        """测试无变化"""
        qian = gua_data["gua_map"]["111111"]
        changed = qian.get_changed_gua([])
        # 无变化应该得到原卦
        assert changed.binary_code == "111111"

    def test_change_involution(self, gua_data):
        """测试两次相同变化回到原卦"""
        for gua in gua_data["all_guas"]:
            # 随机选择1-3个位置变化
            import random

            random.seed(gua.index)  # 固定随机种子以便复现
            positions = random.sample(range(1, 7), random.randint(1, 3))

            changed = gua.get_changed_gua(positions)
            changed_back = changed.get_changed_gua(positions)

            assert changed_back.binary_code == gua.binary_code, (
                f"{gua.name}两次变化后应该回到原卦"
            )


class TestGuaRelations:
    """测试卦象关系的综合性质"""

    def test_qian_all_relations(self, gua_data):
        """测试乾卦的所有关系"""
        qian = gua_data["gua_map"]["111111"]

        # 错卦 -> 坤
        assert qian.get_dui_gua().name == "坤"
        # 综卦 -> 自身
        assert qian.get_zong_gua().binary_code == "111111"
        # 反卦 -> 自身（上下都是乾）
        assert qian.get_fan_gua().binary_code == "111111"
        # 互卦 -> 乾（都是纯阳卦）
        assert qian.get_shang_hu_gua().name == "乾"
        assert qian.get_xia_hu_gua().name == "乾"

    def test_special_pairs(self, gua_data):
        """测试特殊的卦对关系"""
        # 泰卦和否卦
        tai = gua_data["gua_map"]["111000"]  # 地天泰
        pi = gua_data["gua_map"]["000111"]  # 天地否

        # 互为综卦
        assert tai.get_zong_gua().binary_code == pi.binary_code
        assert pi.get_zong_gua().binary_code == tai.binary_code

        # 互为反卦
        assert tai.get_fan_gua().binary_code == pi.binary_code
        assert pi.get_fan_gua().binary_code == tai.binary_code

        # 互为错卦
        assert tai.get_dui_gua().binary_code == pi.binary_code
        assert pi.get_dui_gua().binary_code == tai.binary_code

    @pytest.mark.slow
    def test_all_gua_relations_defined(self, gua_data):
        """测试所有卦的关系都有定义"""
        for gua in gua_data["all_guas"]:
            # 所有关系方法都应该返回有效的卦
            assert gua.get_dui_gua() is not None
            assert gua.get_zong_gua() is not None
            assert gua.get_fan_gua() is not None
            assert gua.get_shang_hu_gua() is not None
            assert gua.get_xia_hu_gua() is not None

            # 变卦测试
            changed = gua.get_changed_gua([1])
            assert changed is not None
