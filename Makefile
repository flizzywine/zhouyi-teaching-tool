# 周易学习程序 - Makefile

.PHONY: test test-unit test-data test-transform coverage clean lint help install

# 默认目标
help:
	@echo "周易学习程序 - 自动化测试命令"
	@echo ""
	@echo "可用命令:"
	@echo "  make install        - 安装依赖"
	@echo "  make test           - 运行所有测试"
	@echo "  make test-unit      - 运行单元测试"
	@echo "  make test-data      - 运行数据完整性测试"
	@echo "  make test-transform - 运行卦象变换测试"
	@echo "  make coverage       - 生成覆盖率报告"
	@echo "  make debug          - 运行调试脚本"
	@echo "  make clean          - 清理测试生成文件"

# 安装依赖
install:
	python3 -m venv venv
	./venv/bin/pip install pytest pytest-cov flet

# 运行所有测试
test:
	./run_tests.sh

# 运行特定测试
test-unit:
	./venv/bin/pytest tests/test_gua_data.py -v

test-data:
	./venv/bin/pytest tests/test_data_completeness.py -v

test-transform:
	./venv/bin/pytest tests/test_gua_transformations.py -v

# 生成覆盖率报告
coverage:
	./venv/bin/pytest tests/ --cov=. --cov-report=html --cov-report=term --cov-report=xml
	@echo "HTML覆盖率报告: htmlcov/index.html"

# 运行调试脚本
debug:
	./venv/bin/python debug_helper.py

# 清理测试生成文件
clean:
	rm -rf htmlcov
	rm -f .coverage
	rm -f coverage.xml
	rm -rf .pytest_cache
	rm -rf tests/__pycache__
	rm -f debug_report.txt
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "清理完成"
