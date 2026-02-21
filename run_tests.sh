#!/bin/bash
# 自动化测试运行脚本

echo "=========================================="
echo "周易学习程序 - 自动化测试"
echo "=========================================="
echo ""

# 检查虚拟环境
if [ -d "venv" ]; then
    echo "[1/4] 激活虚拟环境..."
    source venv/bin/activate
else
    echo "[警告] 虚拟环境不存在，尝试使用系统Python..."
fi

# 运行测试
echo ""
echo "[2/4] 运行单元测试..."
./venv/bin/pytest tests/test_gua_data.py -v --tb=short
UNIT_RESULT=$?

echo ""
echo "[3/4] 运行数据完整性测试..."
./venv/bin/pytest tests/test_data_completeness.py -v --tb=short
DATA_RESULT=$?

echo ""
echo "[4/4] 运行卦象变换测试..."
./venv/bin/pytest tests/test_gua_transformations.py -v --tb=short
TRANS_RESULT=$?

# 生成覆盖率报告
echo ""
echo "[附加] 生成覆盖率报告..."
./venv/bin/pytest tests/ --cov=. --cov-report=html --cov-report=term

# 总结
echo ""
echo "=========================================="
echo "测试结果总结"
echo "=========================================="
if [ $UNIT_RESULT -eq 0 ]; then
    echo "✓ 单元测试: 通过"
else
    echo "✗ 单元测试: 失败"
fi

if [ $DATA_RESULT -eq 0 ]; then
    echo "✓ 数据完整性测试: 通过"
else
    echo "✗ 数据完整性测试: 失败"
fi

if [ $TRANS_RESULT -eq 0 ]; then
    echo "✓ 卦象变换测试: 通过"
else
    echo "✗ 卦象变换测试: 失败"
fi

# 生成调试报告
echo ""
echo "[附加] 生成调试报告..."
./venv/bin/python debug_helper.py --report > debug_report.txt 2>&1
echo "调试报告已保存到 debug_report.txt"

# 返回总结果
if [ $UNIT_RESULT -eq 0 ] && [ $DATA_RESULT -eq 0 ] && [ $TRANS_RESULT -eq 0 ]; then
    echo ""
    echo "🎉 所有测试通过！"
    exit 0
else
    echo ""
    echo "⚠️  部分测试失败，请查看上方输出"
    exit 1
fi
