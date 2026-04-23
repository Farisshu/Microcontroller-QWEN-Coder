#!/usr/bin/env python3
"""
Report Generator for Microcontroller-QWEN-Coder Project

This script generates comprehensive reports from CI/CD pipeline data,
including MISRA compliance, FreeRTOS analysis, test results, and more.

Supports multiple output formats: JSON, HTML, Markdown, and PDF-ready formats.
Designed for internship preparation demonstrating industry best practices.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List


class ReportGenerator:
    """Generate comprehensive project reports in multiple formats."""
    
    def __init__(self, data_file: Optional[str] = None):
        self.data_file = Path(data_file) if data_file else None
        self.report_data: Dict[str, Any] = {}
        
    def load_data(self, data_file: str) -> bool:
        """Load report data from JSON file."""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                self.report_data = json.load(f)
            return True
        except FileNotFoundError:
            print(f"Error: File not found: {data_file}")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format: {e}")
            return False
    
    def generate_summary_report(self) -> str:
        """Generate a human-readable summary report in Markdown format."""
        if not self.report_data:
            return "No data available"
        
        md = []
        md.append("# CI/CD Pipeline Report Summary")
        md.append("")
        md.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md.append("")
        
        # Project Info
        if "report_metadata" in self.report_data:
            meta = self.report_data["report_metadata"]
            md.append("## Project Information")
            md.append(f"- **Project:** {meta.get('project_name', 'N/A')}")
            md.append(f"- **Branch:** {meta.get('branch', 'N/A')}")
            md.append(f"- **Commit:** {meta.get('commit_hash', 'N/A')[:8]}")
            md.append("")
        
        # Overall Status
        if "summary" in self.report_data:
            summary = self.report_data["summary"]
            md.append("## Overall Status")
            md.append("")
            status_emoji = "✅" if summary.get("overall_status") == "passed" else "⚠️"
            md.append(f"{status_emoji} **Status:** {summary.get('overall_status', 'N/A')}")
            md.append(f"**Grade:** {summary.get('grade', 'N/A')}")
            md.append(f"**Ready for Production:** {'Yes' if summary.get('ready_for_production') else 'No'}")
            md.append(f"**Blocking Issues:** {summary.get('blocking_issues', 0)}")
            md.append(f"**Warnings:** {summary.get('warnings_count', 0)}")
            md.append("")
        
        # MISRA Compliance
        if "misra_compliance" in self.report_data:
            misra = self.report_data["misra_compliance"]
            md.append("## MISRA C:2012 Compliance")
            md.append("")
            md.append(f"**Compliance Rate:** {misra.get('compliance_percentage', 0)}%")
            md.append(f"**Rules Passed:** {misra.get('rules_passed', 0)}/{misra.get('rules_checked', 0)}")
            md.append("")
            
            violations = misra.get("violations", [])
            if violations:
                md.append("### Violations")
                md.append("")
                for v in violations[:5]:  # Show first 5
                    md.append(f"- **Rule {v.get('rule_id')}** ({v.get('severity')}): {v.get('description')}")
                    md.append(f"  - File: `{v.get('file')}:{v.get('line')}`")
                md.append("")
        
        # Test Results
        if "test_results" in self.report_data:
            tests = self.report_data["test_results"]
            md.append("## Test Results")
            md.append("")
            md.append(f"**Framework:** {tests.get('framework', 'N/A')}")
            md.append(f"**Total Tests:** {tests.get('total_tests', 0)}")
            md.append(f"**Passed:** {tests.get('tests_passed', 0)}")
            md.append(f"**Failed:** {tests.get('tests_failed', 0)}")
            md.append(f"**Success Rate:** {tests.get('success_rate_percent', 0)}%")
            md.append("")
            
            failed = tests.get("failed_tests", [])
            if failed:
                md.append("### Failed Tests")
                md.append("")
                for test in failed[:5]:
                    md.append(f"- `{test.get('test_name')}` in `{test.get('file')}:{test.get('line')}`")
                    md.append(f"  - Error: {test.get('failure_message')}")
                md.append("")
        
        # FreeRTOS Analysis
        if "freertos_analysis" in self.report_data:
            rtos = self.report_data["freertos_analysis"]
            md.append("## FreeRTOS Analysis")
            md.append("")
            md.append(f"**Version:** {rtos.get('version', 'N/A')}")
            md.append(f"**Status:** {rtos.get('integration_status', 'N/A')}")
            md.append("")
            
            if "task_summary" in rtos:
                tasks = rtos["task_summary"]
                md.append("### Task Summary")
                md.append(f"- Total Tasks: {tasks.get('total_tasks', 0)}")
                if "tasks_by_priority" in tasks:
                    prio = tasks["tasks_by_priority"]
                    md.append(f"- High Priority: {prio.get('high', 0)}")
                    md.append(f"- Medium Priority: {prio.get('medium', 0)}")
                    md.append(f"- Low Priority: {prio.get('low', 0)}")
                md.append("")
        
        # Build Artifacts
        if "build_artifacts" in self.report_data:
            build = self.report_data["build_artifacts"]
            md.append("## Build Information")
            md.append("")
            md.append(f"**Compiler:** {build.get('compiler', 'N/A')} v{build.get('compiler_version', 'N/A')}")
            md.append(f"**Target:** {build.get('target_architecture', 'N/A')}")
            md.append(f"**Optimization:** {build.get('optimization_level', 'N/A')}")
            md.append("")
            
            if "binary_size" in build:
                size = build["binary_size"]
                md.append("### Binary Size")
                md.append(f"- Total Size: {size.get('total_size_bytes', 0):,} bytes")
                md.append(f"- Utilization: {size.get('utilization_percent', 0)}%")
                md.append("")
        
        # Recommendations
        if "recommendations" in self.report_data:
            recs = self.report_data["recommendations"]
            md.append("## Recommendations")
            md.append("")
            
            high_priority = [r for r in recs if r.get("priority") == "high"]
            medium_priority = [r for r in recs if r.get("priority") == "medium"]
            
            if high_priority:
                md.append("### High Priority")
                for rec in high_priority:
                    md.append(f"- [{rec.get('category')}] {rec.get('recommendation')}")
                    md.append(f"  - Estimated Effort: {rec.get('estimated_effort', 'N/A')}")
                md.append("")
            
            if medium_priority:
                md.append("### Medium Priority")
                for rec in medium_priority[:3]:  # Show top 3
                    md.append(f"- [{rec.get('category')}] {rec.get('recommendation')}")
                    md.append(f"  - Estimated Effort: {rec.get('estimated_effort', 'N/A')}")
                md.append("")
        
        return "\n".join(md)
    
    def generate_html_report(self) -> str:
        """Generate an HTML report."""
        if not self.report_data:
            return "<html><body>No data available</body></html>"
        
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html lang='en'>")
        html.append("<head>")
        html.append("<meta charset='UTF-8'>")
        html.append("<title>CI/CD Pipeline Report</title>")
        html.append("<style>")
        html.append("""
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            h1 { color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }
            h2 { color: #555; margin-top: 30px; }
            .status-pass { color: #4CAF50; font-weight: bold; }
            .status-warning { color: #FF9800; font-weight: bold; }
            .status-fail { color: #F44336; font-weight: bold; }
            .metric { display: inline-block; margin: 10px 20px 10px 0; padding: 15px; background: #f9f9f9; border-radius: 4px; }
            .metric-value { font-size: 24px; font-weight: bold; color: #2196F3; }
            .metric-label { font-size: 12px; color: #666; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #4CAF50; color: white; }
            tr:hover { background: #f5f5f5; }
            .recommendation { padding: 10px; margin: 10px 0; border-left: 4px solid #2196F3; background: #e3f2fd; }
            .recommendation.high { border-left-color: #F44336; background: #ffebee; }
            .recommendation.medium { border-left-color: #FF9800; background: #fff3e0; }
        """)
        html.append("</style>")
        html.append("</head>")
        html.append("<body>")
        html.append("<div class='container'>")
        
        # Header
        html.append("<h1>📊 CI/CD Pipeline Report</h1>")
        if "report_metadata" in self.report_data:
            meta = self.report_data["report_metadata"]
            html.append(f"<p><strong>Project:</strong> {meta.get('project_name', 'N/A')}</p>")
            html.append(f"<p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
        
        # Summary
        if "summary" in self.report_data:
            summary = self.report_data["summary"]
            status_class = "status-pass" if summary.get("overall_status") == "passed" else "status-warning"
            html.append(f"<h2>Overall Status</h2>")
            html.append(f"<p class='{status_class}'>{summary.get('overall_status', 'N/A').upper()}</p>")
            html.append("<div>")
            html.append(f"<div class='metric'><div class='metric-value'>{summary.get('grade', 'N/A')}</div><div class='metric-label'>Grade</div></div>")
            html.append(f"<div class='metric'><div class='metric-value'>{summary.get('blocking_issues', 0)}</div><div class='metric-label'>Blocking Issues</div></div>")
            html.append(f"<div class='metric'><div class='metric-value'>{summary.get('warnings_count', 0)}</div><div class='metric-label'>Warnings</div></div>")
            html.append("</div>")
        
        # MISRA
        if "misra_compliance" in self.report_data:
            misra = self.report_data["misra_compliance"]
            html.append("<h2>MISRA C:2012 Compliance</h2>")
            html.append(f"<p><strong>Compliance:</strong> {misra.get('compliance_percentage', 0)}%</p>")
            html.append("<table><tr><th>Rule ID</th><th>Severity</th><th>Description</th><th>File</th></tr>")
            for v in misra.get("violations", [])[:10]:
                html.append(f"<tr><td>{v.get('rule_id', 'N/A')}</td><td>{v.get('severity', 'N/A')}</td><td>{v.get('description', 'N/A')}</td><td>{v.get('file', 'N/A')}:{v.get('line', 'N/A')}</td></tr>")
            html.append("</table>")
        
        # Test Results
        if "test_results" in self.report_data:
            tests = self.report_data["test_results"]
            html.append("<h2>Test Results</h2>")
            html.append(f"<p><strong>Framework:</strong> {tests.get('framework', 'N/A')}</p>")
            html.append("<div>")
            html.append(f"<div class='metric'><div class='metric-value'>{tests.get('total_tests', 0)}</div><div class='metric-label'>Total Tests</div></div>")
            html.append(f"<div class='metric'><div class='metric-value'>{tests.get('tests_passed', 0)}</div><div class='metric-label'>Passed</div></div>")
            html.append(f"<div class='metric'><div class='metric-value'>{tests.get('tests_failed', 0)}</div><div class='metric-label'>Failed</div></div>")
            html.append(f"<div class='metric'><div class='metric-value'>{tests.get('success_rate_percent', 0)}%</div><div class='metric-label'>Success Rate</div></div>")
            html.append("</div>")
        
        # Recommendations
        if "recommendations" in self.report_data:
            html.append("<h2>Recommendations</h2>")
            for rec in self.report_data["recommendations"]:
                priority = rec.get("priority", "low")
                html.append(f"<div class='recommendation {priority}'>")
                html.append(f"<strong>[{priority.upper()}]</strong> {rec.get('recommendation', 'N/A')}")
                html.append(f"<br><em>Estimated Effort: {rec.get('estimated_effort', 'N/A')}</em>")
                html.append("</div>")
        
        html.append("</div>")
        html.append("</body>")
        html.append("</html>")
        
        return "\n".join(html)
    
    def save_report(self, output_path: str, format: str = "json") -> str:
        """Save report to file in specified format."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if format == "json":
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.report_data, f, indent=2)
        elif format == "md":
            content = self.generate_summary_report()
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
        elif format == "html":
            content = self.generate_html_report()
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return str(output_file)


def main():
    """Main entry point for report generation."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive CI/CD pipeline reports"
    )
    parser.add_argument(
        "-i", "--input",
        default=None,
        help="Input JSON data file (default: use example data)"
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output file path (default: reports/report_TIMESTAMP.ext)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["json", "md", "html"],
        default="md",
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--show-summary",
        action="store_true",
        help="Display summary to console"
    )
    
    args = parser.parse_args()
    
    generator = ReportGenerator()
    
    # Load data
    if args.input:
        if not generator.load_data(args.input):
            sys.exit(1)
    else:
        # Use example data
        example_path = Path(__file__).parent.parent / "data" / "example_report.json"
        if example_path.exists():
            generator.load_data(str(example_path))
            print(f"Loaded example data from: {example_path}")
        else:
            print("Error: No input file provided and example data not found")
            sys.exit(1)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        reports_dir = Path(__file__).parent.parent / "reports"
        reports_dir.mkdir(exist_ok=True)
        output_path = reports_dir / f"report_{timestamp}.{args.format}"
    
    # Generate and save report
    output_file = generator.save_report(str(output_path), format=args.format)
    print(f"\n✓ Report generated: {output_file}")
    
    # Show summary if requested
    if args.show_summary:
        print("\n" + "=" * 60)
        print("REPORT SUMMARY")
        print("=" * 60)
        print(generator.generate_summary_report())
    
    print(f"\nReport successfully generated!")


if __name__ == "__main__":
    main()
