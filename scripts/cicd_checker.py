#!/usr/bin/env python3
"""
CI/CD Pipeline Checker for Microcontroller-QWEN-Coder Project

This script performs comprehensive checks for:
- Code quality and MISRA compliance indicators
- FreeRTOS integration validation
- Build system verification
- Test coverage analysis
- Documentation completeness

Designed for internship preparation demonstrating industry best practices.
"""

import os
import sys
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class CICDChecker:
    """Main class for CI/CD pipeline checking and validation."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.results: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root.absolute()),
            "checks": {},
            "summary": {
                "total_checks": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0
            }
        }
        
        # MISRA C:2012 critical rules indicators (simplified check)
        self.misra_critical_rules = [
            "rule_5_1",  # External identifiers uniqueness
            "rule_8_1",  # Functions should not be defined with unused parameters
            "rule_10_1", # Operands shall not be of inappropriate essential type
            "rule_11_1", # Conversions shall not be performed between pointer types
            "rule_13_1", # Initialization lists shall not contain persistent side effects
            "rule_14_1", # Loop counters shall not be modified within loop body
            "rule_17_1", # Functions shall not be recursive
            "rule_21_1", # Standard library functions usage restrictions
        ]
        
    def check_directory_structure(self) -> Dict[str, Any]:
        """Verify expected directory structure exists."""
        check_result = {
            "name": "Directory Structure",
            "status": "PASS",
            "details": [],
            "warnings": []
        }
        
        expected_dirs = ["src", "include", "tests", "docs", "scripts"]
        missing_dirs = []
        
        for dir_name in expected_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                check_result["details"].append(f"✓ Directory '{dir_name}' exists")
            else:
                missing_dirs.append(dir_name)
                check_result["warnings"].append(f"⚠ Directory '{dir_name}' not found")
        
        if missing_dirs:
            check_result["status"] = "WARNING"
            check_result["details"].append(f"Missing directories: {', '.join(missing_dirs)}")
        
        return check_result
    
    def check_source_files(self) -> Dict[str, Any]:
        """Check for source code files and basic structure."""
        check_result = {
            "name": "Source Files Analysis",
            "status": "PASS",
            "details": [],
            "warnings": [],
            "metrics": {}
        }
        
        src_dir = self.project_root / "src"
        include_dir = self.project_root / "include"
        
        c_files = list(src_dir.glob("*.c")) if src_dir.exists() else []
        h_files = list(include_dir.glob("*.h")) if include_dir.exists() else []
        h_files.extend(src_dir.glob("*.h"))
        
        check_result["metrics"]["c_files_count"] = len(c_files)
        check_result["metrics"]["h_files_count"] = len(h_files)
        check_result["metrics"]["total_lines"] = 0
        
        if not c_files:
            check_result["status"] = "WARNING"
            check_result["warnings"].append("No .c source files found in src/")
            check_result["details"].append("⚠ No source files detected - this may be a new project")
        else:
            check_result["details"].append(f"✓ Found {len(c_files)} C source files")
            check_result["details"].append(f"✓ Found {len(h_files)} header files")
            
            # Count lines and check for basic patterns
            total_lines = 0
            freertos_usage = False
            misra_violations_indicators = 0
            
            for file_path in c_files + h_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.split('\n')
                        total_lines += len(lines)
                        
                        # Check for FreeRTOS usage
                        if any(pattern in content for pattern in 
                               ['#include "FreeRTOS.h"', 'xTaskCreate', 'vTaskDelay', 
                                'xQueueCreate', 'xSemaphoreCreate']):
                            freertos_usage = True
                        
                        # Basic MISRA indicators (simplified)
                        if 'goto' in content:
                            misra_violations_indicators += 1
                        if re.search(r'\bmalloc\s*\(', content):
                            misra_violations_indicators += 1
                            
                except Exception as e:
                    check_result["warnings"].append(f"Error reading {file_path}: {str(e)}")
            
            check_result["metrics"]["total_lines"] = total_lines
            check_result["metrics"]["freertos_detected"] = freertos_usage
            check_result["metrics"]["potential_misra_issues"] = misra_violations_indicators
            
            if freertos_usage:
                check_result["details"].append("✓ FreeRTOS integration detected")
            else:
                check_result["warnings"].append("ℹ No FreeRTOS usage detected")
            
            if misra_violations_indicators > 0:
                check_result["warnings"].append(
                    f"⚠ {misra_violations_indicators} potential MISRA compliance issues detected"
                )
            else:
                check_result["details"].append("✓ No obvious MISRA violations detected")
        
        return check_result
    
    def check_freertos_integration(self) -> Dict[str, Any]:
        """Validate FreeRTOS integration patterns."""
        check_result = {
            "name": "FreeRTOS Integration Check",
            "status": "INFO",
            "details": [],
            "requirements": []
        }
        
        freertos_requirements = [
            ("FreeRTOS.h header", '#include "FreeRTOS.h"'),
            ("Task definitions", 'xTaskCreate'),
            ("Scheduler start", 'vTaskStartScheduler'),
            ("Task delays", 'vTaskDelay'),
            ("Queues or Semaphores", ['xQueueCreate', 'xSemaphoreCreate']),
        ]
        
        found_requirements = []
        missing_requirements = []
        
        # Search all source files
        all_source = list(self.project_root.glob("**/*.c")) + \
                     list(self.project_root.glob("**/*.h"))
        
        all_content = ""
        for file_path in all_source:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    all_content += f.read() + "\n"
            except:
                pass
        
        for req_name, req_pattern in freertos_requirements:
            if isinstance(req_pattern, list):
                found = any(p in all_content for p in req_pattern)
            else:
                found = req_pattern in all_content
            
            if found:
                found_requirements.append(req_name)
                check_result["details"].append(f"✓ {req_name} found")
            else:
                missing_requirements.append(req_name)
                check_result["details"].append(f"ℹ {req_name} not found")
        
        if len(found_requirements) >= 3:
            check_result["status"] = "PASS"
        elif len(found_requirements) > 0:
            check_result["status"] = "WARNING"
        else:
            check_result["status"] = "INFO"
            check_result["details"].append("ℹ This is acceptable for projects not using FreeRTOS")
        
        check_result["requirements"] = {
            "found": found_requirements,
            "missing": missing_requirements,
            "completion_percentage": round(len(found_requirements) / len(freertos_requirements) * 100, 2)
        }
        
        return check_result
    
    def check_ci_cd_config(self) -> Dict[str, Any]:
        """Check for CI/CD configuration files."""
        check_result = {
            "name": "CI/CD Configuration",
            "status": "PASS",
            "details": [],
            "warnings": [],
            "files_found": []
        }
        
        ci_cd_patterns = [
            ".github/workflows/*.yml",
            ".github/workflows/*.yaml",
            ".gitlab-ci.yml",
            ".travis.yml",
            "Jenkinsfile",
            ".circleci/config.yml",
            "azure-pipelines.yml"
        ]
        
        found_files = []
        for pattern in ci_cd_patterns:
            matches = list(self.project_root.glob(pattern))
            found_files.extend([str(f.relative_to(self.project_root)) for f in matches])
        
        if found_files:
            check_result["files_found"] = found_files
            check_result["details"].append(f"✓ Found CI/CD config: {', '.join(found_files)}")
        else:
            check_result["status"] = "WARNING"
            check_result["details"].append("⚠ No CI/CD configuration files found")
            check_result["details"].append("ℹ Consider adding GitHub Actions workflow in .github/workflows/")
        
        # Check for Makefile or build system
        build_files = ["Makefile", "makefile", "CMakeLists.txt", "meson.build"]
        found_build = [f for f in build_files if (self.project_root / f).exists()]
        
        if found_build:
            check_result["details"].append(f"✓ Build system found: {', '.join(found_build)}")
        else:
            check_result["warnings"].append("⚠ No standard build system file found")
        
        return check_result
    
    def check_test_coverage(self) -> Dict[str, Any]:
        """Analyze test structure and coverage indicators."""
        check_result = {
            "name": "Test Coverage Analysis",
            "status": "PASS",
            "details": [],
            "warnings": [],
            "metrics": {}
        }
        
        tests_dir = self.project_root / "tests"
        
        if not tests_dir.exists():
            check_result["status"] = "WARNING"
            check_result["details"].append("⚠ No tests/ directory found")
            check_result["metrics"]["test_files"] = 0
            return check_result
        
        test_files = list(tests_dir.glob("*.c")) + \
                     list(tests_dir.glob("*.cpp")) + \
                     list(tests_dir.glob("*.py"))
        
        check_result["metrics"]["test_files"] = len(test_files)
        check_result["details"].append(f"✓ Found {len(test_files)} test files")
        
        # Check for test framework indicators
        test_frameworks = {
            "Unity": ["unity.h", "TEST_ASSERT"],
            "CppUTest": ["CppUTest/TestHarness.h"],
            "Google Test": ["gtest/gtest.h", "TEST("],
            "pytest": ["import pytest", "def test_"]
        }
        
        detected_frameworks = []
        all_test_content = ""
        
        for test_file in test_files:
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    all_test_content += content + "\n"
            except:
                pass
        
        for framework, patterns in test_frameworks.items():
            if any(p in all_test_content for p in patterns):
                detected_frameworks.append(framework)
        
        if detected_frameworks:
            check_result["details"].append(f"✓ Test frameworks detected: {', '.join(detected_frameworks)}")
        else:
            check_result["warnings"].append("ℹ No standard test framework detected")
        
        # Estimate coverage (simplified)
        src_files = list((self.project_root / "src").glob("*.c"))
        if src_files and test_files:
            ratio = len(test_files) / len(src_files)
            check_result["metrics"]["test_to_source_ratio"] = round(ratio, 2)
            if ratio >= 1.0:
                check_result["details"].append("✓ Good test-to-source ratio")
            elif ratio >= 0.5:
                check_result["details"].append("ℹ Moderate test coverage")
            else:
                check_result["warnings"].append("⚠ Low test-to-source ratio")
        
        return check_result
    
    def check_documentation(self) -> Dict[str, Any]:
        """Check documentation completeness."""
        check_result = {
            "name": "Documentation Check",
            "status": "PASS",
            "details": [],
            "files_found": []
        }
        
        doc_files = ["README.md", "LICENSE", "CONTRIBUTING.md", "CHANGELOG.md"]
        docs_dir = self.project_root / "docs"
        
        found_docs = []
        missing_docs = []
        
        for doc_file in doc_files:
            if (self.project_root / doc_file).exists():
                found_docs.append(doc_file)
                check_result["details"].append(f"✓ {doc_file} present")
            else:
                missing_docs.append(doc_file)
                check_result["details"].append(f"ℹ {doc_file} not found")
        
        if docs_dir.exists():
            doc_files_in_dir = list(docs_dir.glob("*.md"))
            if doc_files_in_dir:
                check_result["details"].append(f"✓ docs/ directory contains {len(doc_files_in_dir)} files")
                found_docs.append(f"docs/ ({len(doc_files_in_dir)} files)")
        
        if "README.md" not in found_docs:
            check_result["status"] = "WARNING"
            check_result["details"].append("⚠ README.md is recommended for all projects")
        
        check_result["files_found"] = found_docs
        check_result["completeness"] = round(len(found_docs) / (len(doc_files) + 1) * 100, 2)
        
        return check_result
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Execute all checks and compile results."""
        print("=" * 60)
        print("CI/CD Pipeline Checker - Microcontroller-QWEN-Coder")
        print("=" * 60)
        print(f"\nProject Root: {self.project_root.absolute()}")
        print(f"Timestamp: {self.results['timestamp']}\n")
        
        checks = [
            ("Directory Structure", self.check_directory_structure),
            ("Source Files Analysis", self.check_source_files),
            ("FreeRTOS Integration", self.check_freertos_integration),
            ("CI/CD Configuration", self.check_ci_cd_config),
            ("Test Coverage", self.check_test_coverage),
            ("Documentation", self.check_documentation),
        ]
        
        for check_name, check_func in checks:
            print(f"\nRunning: {check_name}...")
            result = check_func()
            self.results["checks"][check_name] = result
            
            status_symbol = "✓" if result["status"] == "PASS" else ("⚠" if result["status"] == "WARNING" else "ℹ")
            print(f"  {status_symbol} Status: {result['status']}")
            
            for detail in result.get("details", [])[:3]:  # Show first 3 details
                print(f"    {detail}")
            
            # Update summary
            self.results["summary"]["total_checks"] += 1
            if result["status"] == "PASS":
                self.results["summary"]["passed"] += 1
            elif result["status"] == "WARNING":
                self.results["summary"]["warnings"] += 1
            else:
                self.results["summary"]["failed"] += 1
        
        # Print summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total Checks: {self.results['summary']['total_checks']}")
        print(f"Passed: {self.results['summary']['passed']}")
        print(f"Warnings: {self.results['summary']['warnings']}")
        print(f"Failed: {self.results['summary']['failed']}")
        
        success_rate = (self.results["summary"]["passed"] / 
                       self.results["summary"]["total_checks"] * 100)
        print(f"Success Rate: {success_rate:.1f}%")
        
        return self.results
    
    def save_report(self, output_path: Optional[str] = None) -> str:
        """Save results to JSON file."""
        if output_path is None:
            output_dir = self.project_root / "reports"
            output_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = output_dir / f"cicd_report_{timestamp}.json"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n✓ Report saved to: {output_path}")
        return str(output_path)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="CI/CD Pipeline Checker for Microcontroller Projects"
    )
    parser.add_argument(
        "-p", "--project-root",
        default=".",
        help="Root directory of the project (default: current directory)"
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output path for JSON report (default: reports/cicd_report_TIMESTAMP.json)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress detailed output, only show summary"
    )
    
    args = parser.parse_args()
    
    checker = CICDChecker(project_root=args.project_root)
    results = checker.run_all_checks()
    
    if not args.quiet:
        output_file = checker.save_report(args.output)
    
    # Exit with appropriate code
    if results["summary"]["failed"] > 0:
        sys.exit(1)
    elif results["summary"]["warnings"] > 0:
        sys.exit(0)  # Warnings don't fail the build
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
