# 自动化测试使用指南

## 快速开始

### 运行所有测试
```bash
./run_tests.sh
```

或使用 Make:
```bash
make test
```

## 测试结构

### 测试文件说明

| 文件 | 描述 |
|------|------|
| `tests/test_gua_data.py` | 核心数据结构和算法单元测试 |
| `tests/test_data_completeness.py` | 64卦数据完整性验证 |
| `tests/test_gua_transformations.py` | 卦象变换算法集成测试 |

### 测试覆盖范围

**单元测试 (test_gua_data.py)**
- Yao类（爻）的创建、翻转
- Gua类（卦）的基本属性
- binary_to_gua函数
- search_gua搜索功能
- get_gua_by_index索引查询

**数据完整性测试 (test_data_completeness.py)**
- 64卦数量验证
- 索引唯一性
- 二进制编码有效性
- 所有字段非空检查
- 特定卦数据验证
- 数据一致性检查

**卦象变换测试 (test_gua_transformations.py)**
- 错卦（对卦）验证
- 综卦验证
- 反卦验证
- 互卦（上互卦、下互卦）验证
- 变卦验证
- 特殊卦对关系验证

## Make 命令

```bash
make install        # 安装依赖
make test           # 运行所有测试
make test-unit      # 仅运行单元测试
make test-data      # 仅运行数据测试
make test-transform # 仅运行变换测试
make coverage       # 生成覆盖率报告
make debug          # 运行调试脚本
make clean          # 清理测试文件
make help           # 显示帮助
```

## 调试工具

### debug_helper.py - 调试辅助脚本

```bash
# 运行所有检查
python debug_helper.py --check

# 查看特定卦的信息
python debug_helper.py --gua 乾

# 列出所有卦
python debug_helper.py --list

# 生成调试报告
python debug_helper.py --report
```

## 测试覆盖率

运行测试后，会生成覆盖率报告：

- **HTML报告**: `htmlcov/index.html`
- **XML报告**: `coverage.xml`
- **终端报告**: 测试运行时显示

## Pytest 标记

测试使用了以下标记：

- `@pytest.mark.unit` - 单元测试
- `@pytest.mark.integration` - 集成测试
- `@pytest.mark.data` - 数据验证测试
- `@pytest.mark.slow` - 慢速测试

运行特定标记的测试：
```bash
./venv/bin/pytest -m unit    # 仅运行单元测试
./venv/bin/pytest -m slow    # 包含慢速测试
```

## 测试配置

测试配置在 `pytest.ini` 文件中：
- 测试路径: `tests/`
- 测试文件模式: `test_*.py`
- 自动覆盖率报告
- 详细的失败信息

## 虚拟环境

项目使用虚拟环境 `venv/`，包含：
- pytest - 测试框架
- pytest-cov - 覆盖率工具
- flet - UI框架

激活虚拟环境：
```bash
source venv/bin/activate
```

## 持续集成

可将以下命令集成到CI/CD：

```bash
# 安装依赖
python3 -m venv venv
./venv/bin/pip install pytest pytest-cov flet

# 运行测试
./venv/bin/pytest tests/ --cov=. --cov-report=xml

# 检查测试是否通过
if [ $? -eq 0 ]; then
    echo "测试通过"
else
    echo "测试失败"
    exit 1
fi
```

## 常见问题

**Q: 测试失败如何调试？**
A: 使用 `./run_tests.sh` 会显示详细的错误信息，或使用 `python debug_helper.py --gua <卦名>` 查看具体卦的信息。

**Q: 如何添加新测试？**
A: 在 `tests/` 目录下创建新的 `test_*.py` 文件，pytest 会自动发现并运行。

**Q: 覆盖率太低怎么办？**
A: 当前 `main.py` 的UI代码覆盖率较低是正常的，因为它是Flet GUI应用。重点保证 `gua_data.py` 的核心算法有良好覆盖。
