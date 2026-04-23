# Makefile for Microcontroller-QWEN-Coder Project
# CI/CD Pipeline and Report Generation Tools
#
# This Makefile provides convenient commands for running CI/CD checks
# and generating reports for internship preparation.

.PHONY: all check report clean help test build

# Default target
all: check report

# Run CI/CD pipeline checker
check:
	@echo "========================================"
	@echo "Running CI/CD Pipeline Checker..."
	@echo "========================================"
	python3 scripts/cicd_checker.py -p . -o reports/cicd_check_result.json

# Generate report from example data
report:
	@echo "========================================"
	@echo "Generating Reports..."
	@echo "========================================"
	python3 scripts/generate_report.py \
		-i data/example_report.json \
		-f md \
		-o reports/summary_report.md \
		--show-summary
	python3 scripts/generate_report.py \
		-i data/example_report.json \
		-f html \
		-o reports/summary_report.html

# Generate report from actual CI/CD check results
report-from-check:
	@echo "========================================"
	@echo "Generating Report from CI/CD Check..."
	@echo "========================================"
	python3 scripts/generate_report.py \
		-i reports/cicd_check_result.json \
		-f md \
		-o reports/check_report.md

# Run all tests
test:
	@echo "========================================"
	@echo "Running Tests..."
	@echo "========================================"
	@if [ -d "tests" ] && [ "$$(ls -A tests)" ]; then \
		pytest tests/ --cov=src --cov-report=html; \
	else \
		echo "No tests found in tests/ directory"; \
	fi

# Build project (placeholder for embedded build)
build:
	@echo "========================================"
	@echo "Building Project..."
	@echo "========================================"
	@if [ -f "Makefile" ] && [ "$$(grep -c '^build:' Makefile 2>/dev/null || echo 0)" -gt 0 ]; then \
		$(MAKE) _build_actual; \
	elif [ -f "CMakeLists.txt" ]; then \
		mkdir -p build && cd build && cmake .. && make; \
	else \
		echo "No build system configured yet."; \
		echo "Create a Makefile or CMakeLists.txt to enable building."; \
	fi

_build_actual:
	@echo "Running actual build..."
	make all

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	rm -rf reports/*.json reports/*.md reports/*.html
	rm -rf build/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	@echo "Clean complete."

# Show help
help:
	@echo "========================================"
	@echo "Microcontroller-QWEN-Coder - Makefile Help"
	@echo "========================================"
	@echo ""
	@echo "Available targets:"
	@echo "  all              - Run checks and generate reports (default)"
	@echo "  check            - Run CI/CD pipeline checker"
	@echo "  report           - Generate reports from example data"
	@echo "  report-from-check- Generate report from actual CI/CD check results"
	@echo "  test             - Run unit tests"
	@echo "  build            - Build the project"
	@echo "  clean            - Remove generated files"
	@echo "  help             - Show this help message"
	@echo ""
	@echo "Data Analysis Targets (NEW):"
	@echo "  generate-data    - Generate demo sensor data (RS485 & CAN)"
	@echo "  analyze-data     - Analyze RS485 demo data with charts"
	@echo "  analyze-can      - Analyze CAN bus demo data"
	@echo "  demo-full        - Complete workflow: generate + analyze"
	@echo "  analyze-custom   - Analyze your own serial data (FILE=param)"
	@echo ""
	@echo "Examples:"
	@echo "  make check       - Run CI/CD checks only"
	@echo "  make report      - Generate reports only"
	@echo "  make all         - Run both checks and reports"
	@echo "  make demo-full   - Full data analysis demo"
	@echo "  make analyze-custom FILE=data/my_serial_log.csv"
	@echo "  make clean       - Clean all generated files"
	@echo ""
	@echo "For more information, see README.md"

# Quick validation for internship demo
demo:
	@echo "========================================"
	@echo "Internship Demo - Quick Validation"
	@echo "========================================"
	@echo ""
	@python3 scripts/cicd_checker.py -p . --quiet
	@echo ""
	@echo "Sample Report Preview:"
	@echo "----------------------------------------"
	@head -30 reports/summary_report.md 2>/dev/null || python3 scripts/generate_report.py -i data/example_report.json -f md -o reports/summary_report.md && head -30 reports/summary_report.md
	@echo ""
	@echo "========================================"
	@echo "Demo Complete!"
	@echo "========================================"

# Generate demo data for serial monitor analysis
generate-data:
	@echo "🔧 Generating demo sensor data..."
	@python tools/generate_demo_data.py

# Run data analyzer on RS485 demo samples
analyze-data:
	@echo "📊 Analyzing RS485 demo data..."
	@python tools/data_analyzer.py -i data/demo_samples/esp32_rs485_demo.csv -f all

# Run data analyzer on CAN bus demo samples
analyze-can:
	@echo "🚗 Analyzing CAN bus demo data..."
	@python tools/data_analyzer.py -i data/demo_samples/mcp2515_can_demo.csv -f all --no-graph

# Full demo workflow with data generation and analysis
demo-full: generate-data analyze-data
	@echo ""
	@echo "✅ Complete demo workflow finished!"
	@echo "📁 Check reports/ directory for HTML and JSON reports"
	@echo "🌐 Open reports/data_analysis_report.html in your browser"

# Analyze custom serial data (usage: make analyze-custom FILE=path/to/your/data.csv)
analyze-custom:
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Error: FILE parameter required. Usage: make analyze-custom FILE=path/to/data.csv"; \
		exit 1; \
	fi
	@echo "📊 Analyzing custom data: $(FILE)"
	@python tools/data_analyzer.py -i $(FILE) -f all
