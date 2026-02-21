#!/usr/bin/env python3
"""
调试辅助脚本
用于诊断和调试周易学习程序的问题
"""

import sys
import os
import argparse
from typing import List, Optional

# 确保能导入项目模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gua_data import ALL_GUAS, GUA_MAP, binary_to_gua, search_gua, init_data
    from gua_data import Yao, Gua, YaoType, TRIGRAMS
except ImportError as e:
    print(f"错误: 无法导入gua_data模块: {e}")
    print("请确保在项目根目录运行此脚本")
    sys.exit(1)


class DebugHelper:
    """调试辅助类"""

    def __init__(self):
        init_data()
        self.errors = []
        self.warnings = []

    def check_data_integrity(self) -> bool:
        """检查数据完整性"""
        print("=" * 60)
        print("检查数据完整性")
        print("=" * 60)

        all_ok = True

        # 检查64卦数量
        if len(ALL_GUAS) != 64:
            self.errors.append(f"卦象数量错误: 期望64，实际{len(ALL_GUAS)}")
            all_ok = False
        else:
            print(f"✓ 卦象数量正确: {len(ALL_GUAS)}")

        # 检查索引唯一性
        indices = [g.index for g in ALL_GUAS]
        if len(indices) != len(set(indices)):
            self.errors.append("卦象索引不唯一")
            all_ok = False
        else:
            print("✓ 卦象索引唯一")

        # 检查二进制编码
        codes = [g.binary_code for g in ALL_GUAS]
        if len(codes) != len(set(codes)):
            self.errors.append("二进制编码不唯一")
            all_ok = False
        else:
            print("✓ 二进制编码唯一")

        # 检查每个卦的数据
        for gua in ALL_GUAS:
            if not self._check_single_gua(gua):
                all_ok = False

        return all_ok

    def _check_single_gua(self, gua: Gua) -> bool:
        """检查单个卦的数据"""
        ok = True

        # 检查基本字段
        if not gua.name:
            self.errors.append(f"卦{gua.index}: 名称为空")
            ok = False

        if not gua.chinese_name:
            self.errors.append(f"卦{gua.index}: 中文名为空")
            ok = False

        if not gua.description:
            self.warnings.append(f"卦{gua.name}: 卦辞为空")

        # 检查爻
        if len(gua.yaos) != 6:
            self.errors.append(f"卦{gua.name}: 爻数量错误(期望6，实际{len(gua.yaos)})")
            ok = False
        else:
            positions = [y.position for y in gua.yaos]
            if set(positions) != {1, 2, 3, 4, 5, 6}:
                self.errors.append(f"卦{gua.name}: 爻位置错误")
                ok = False

        # 检查二进制编码
        if len(gua.binary_code) != 6 or not set(gua.binary_code).issubset({"0", "1"}):
            self.errors.append(f"卦{gua.name}: 二进制编码无效({gua.binary_code})")
            ok = False

        return ok

    def check_transformations(self) -> bool:
        """检查卦象变换算法"""
        print("\n" + "=" * 60)
        print("检查卦象变换算法")
        print("=" * 60)

        all_ok = True

        # 测试错卦的对合性
        for gua in ALL_GUAS:
            dui = gua.get_dui_gua()
            dui_dui = dui.get_dui_gua()
            if dui_dui.binary_code != gua.binary_code:
                self.errors.append(f"{gua.name}: 错卦对合性失败")
                all_ok = False

        if all_ok:
            print("✓ 错卦对合性检查通过")

        # 测试综卦的对合性
        for gua in ALL_GUAS:
            zong = gua.get_zong_gua()
            zong_zong = zong.get_zong_gua()
            if zong_zong.binary_code != gua.binary_code:
                self.errors.append(f"{gua.name}: 综卦对合性失败")
                all_ok = False

        if all_ok:
            print("✓ 综卦对合性检查通过")

        # 测试反卦的对合性
        for gua in ALL_GUAS:
            fan = gua.get_fan_gua()
            fan_fan = fan.get_fan_gua()
            if fan_fan.binary_code != gua.binary_code:
                self.errors.append(f"{gua.name}: 反卦对合性失败")
                all_ok = False

        if all_ok:
            print("✓ 反卦对合性检查通过")

        return all_ok

    def check_special_pairs(self) -> bool:
        """检查特殊卦对关系"""
        print("\n" + "=" * 60)
        print("检查特殊卦对")
        print("=" * 60)

        all_ok = True

        # 检查乾卦和坤卦
        try:
            qian = GUA_MAP["111111"]
            kun = GUA_MAP["000000"]

            if qian.get_dui_gua().binary_code != "000000":
                self.errors.append("乾卦错卦不是坤卦")
                all_ok = False
            else:
                print("✓ 乾卦错卦是坤卦")

            if kun.get_dui_gua().binary_code != "111111":
                self.errors.append("坤卦错卦不是乾卦")
                all_ok = False
            else:
                print("✓ 坤卦错卦是乾卦")

        except KeyError as e:
            self.errors.append(f"找不到特殊卦: {e}")
            all_ok = False

        # 检查泰卦和否卦
        try:
            tai = GUA_MAP["111000"]  # 地天泰
            pi = GUA_MAP["000111"]  # 天地否

            if tai.get_zong_gua().binary_code != pi.binary_code:
                self.errors.append("泰卦综卦不是否卦")
                all_ok = False
            else:
                print("✓ 泰卦和否卦互为综卦")

            if tai.get_fan_gua().binary_code != pi.binary_code:
                self.errors.append("泰卦反卦不是否卦")
                all_ok = False
            else:
                print("✓ 泰卦和否卦互为反卦")

        except KeyError as e:
            self.errors.append(f"找不到特殊卦: {e}")
            all_ok = False

        return all_ok

    def print_summary(self):
        """打印调试摘要"""
        print("\n" + "=" * 60)
        print("调试摘要")
        print("=" * 60)

        if self.errors:
            print(f"\n发现 {len(self.errors)} 个错误:")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
        else:
            print("\n✓ 未发现错误")

        if self.warnings:
            print(f"\n发现 {len(self.warnings)} 个警告:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")

    def generate_report(self, filename: str = "debug_report.txt"):
        """生成调试报告"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write("周易学习程序调试报告\n")
            f.write("=" * 60 + "\n\n")

            f.write("数据完整性检查:\n")
            f.write(f"  - 卦象数量: {len(ALL_GUAS)}\n")
            f.write(f"  - 错误数: {len(self.errors)}\n")
            f.write(f"  - 警告数: {len(self.warnings)}\n\n")

            if self.errors:
                f.write("错误列表:\n")
                for error in self.errors:
                    f.write(f"  - {error}\n")
                f.write("\n")

            if self.warnings:
                f.write("警告列表:\n")
                for warning in self.warnings:
                    f.write(f"  - {warning}\n")
                f.write("\n")

            f.write("所有卦象:\n")
            for gua in ALL_GUAS:
                f.write(
                    f"  {gua.index:2d}. {gua.name} ({gua.chinese_name}) - {gua.binary_code}\n"
                )

        print(f"\n报告已保存到: {filename}")

    def run_all_checks(self) -> bool:
        """运行所有检查"""
        ok1 = self.check_data_integrity()
        ok2 = self.check_transformations()
        ok3 = self.check_special_pairs()
        self.print_summary()
        return ok1 and ok2 and ok3


def print_gua_info(name: str):
    """打印特定卦的详细信息"""
    results = search_gua(name)
    if not results:
        print(f"未找到卦: {name}")
        return

    for gua in results:
        print("\n" + "=" * 60)
        print(f"卦名: {gua.name} ({gua.chinese_name})")
        print("=" * 60)
        print(f"序号: {gua.index}")
        print(f"二进制: {gua.binary_code}")
        print(f"上卦: {gua.upper_gua}")
        print(f"下卦: {gua.lower_gua}")
        print(f"\n卦辞: {gua.description}")
        print(f"\n彖曰: {gua.tuan}")
        print(f"\n象曰: {gua.xiang}")
        print("\n六爻:")
        for yao in reversed(gua.yaos):  # 从上往下显示
            symbol = "—" if yao.is_yang else "- -"
            print(f"  {yao.position}爻 {symbol}: {yao.text}")

        print("\n卦象关系:")
        print(f"  错卦: {gua.get_dui_gua().name}")
        print(f"  综卦: {gua.get_zong_gua().name}")
        print(f"  反卦: {gua.get_fan_gua().name}")
        print(f"  上互卦: {gua.get_shang_hu_gua().name}")
        print(f"  下互卦: {gua.get_xia_hu_gua().name}")


def main():
    parser = argparse.ArgumentParser(description="周易学习程序调试工具")
    parser.add_argument("--check", action="store_true", help="运行所有检查")
    parser.add_argument("--report", action="store_true", help="生成调试报告")
    parser.add_argument("--gua", type=str, help="查看特定卦的信息")
    parser.add_argument("--list", action="store_true", help="列出所有卦")

    args = parser.parse_args()

    if args.gua:
        print_gua_info(args.gua)
        return

    if args.list:
        print("\n所有64卦:")
        print("=" * 60)
        init_data()
        for gua in ALL_GUAS:
            print(
                f"{gua.index:2d}. {gua.name:4s} ({gua.chinese_name}) - {gua.binary_code}"
            )
        return

    # 默认运行检查
    helper = DebugHelper()
    success = helper.run_all_checks()

    if args.report:
        helper.generate_report()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
