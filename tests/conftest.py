"""
Pytest 配置文件
"""

import pytest
import sys
import os

# 确保项目根目录在路径中
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


@pytest.fixture(scope="session")
def gua_data():
    """提供卦象数据的fixture"""
    from gua_data import ALL_GUAS, GUA_MAP, init_data

    init_data()
    return {"all_guas": ALL_GUAS, "gua_map": GUA_MAP}


@pytest.fixture
def sample_gua_qian(gua_data):
    """提供乾卦作为示例"""
    return gua_data["gua_map"]["111111"]


@pytest.fixture
def sample_gua_kun(gua_data):
    """提供坤卦作为示例"""
    return gua_data["gua_map"]["000000"]
