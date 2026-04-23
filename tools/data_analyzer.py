#!/usr/bin/env python3
"""
Data Analyzer and Report Generator
Analyzes serial monitor data from ESP32+RS485 or MCP2515 CAN projects
Generates: Tables, Statistics, Graphs (ASCII & HTML), and Comprehensive Reports
"""

import csv
import json
import argparse
import datetime
from collections import defaultdict
import os

class DataAnalyzer:
    def __init__(self, input_file):
        self.input_file = input_file
        self.data = []
        self.statistics = {}
        self.detect_format()
    
    def detect_format(self):
        """Auto-detect if data is RS485/Modbus or CAN bus format"""
        with open(self.input_file, 'r') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            
            if 'modbus_address' in headers or 'sensor_type' in headers:
                self.format_type = 'RS485_MODBUS'
                print("📡 Detected: RS485/Modbus sensor data")
            elif 'can_id' in headers or 'can_id_hex' in headers:
                self.format_type = 'CAN_BUS'
                print("🚗 Detected: CAN bus message data")
            else:
                raise ValueError("Unknown data format. Expected RS485 or CAN bus data.")
        
        self.load_data()
    
    def load_data(self):
        """Load CSV data into memory"""
        with open(self.input_file, 'r') as f:
            reader = csv.DictReader(f)
            self.data = list(reader)
        print(f"✓ Loaded {len(self.data)} records from {self.input_file}")
    
    def calculate_statistics(self):
        """Compute comprehensive statistics"""
        stats = {
            'total_records': len(self.data),
            'format_type': self.format_type,
            'analysis_timestamp': datetime.datetime.now().isoformat(),
            'time_range': {},
            'error_summary': {},
            'value_statistics': defaultdict(dict),
            'device_summary': defaultdict(int),
            'status_distribution': defaultdict(int)
        }
        
        if not self.data:
            return stats
        
        # Time range analysis
        timestamps = [row['timestamp'] for row in self.data]
        stats['time_range']['start'] = min(timestamps)
        stats['time_range']['end'] = max(timestamps)
        
        # Status distribution
        for row in self.data:
            status = row.get('status', row.get('bus_status', 'UNKNOWN'))
            stats['status_distribution'][status] += 1
            
            # Device/ID summary
            if 'device_id' in row:
                stats['device_summary'][row['device_id']] += 1
            elif 'can_id_hex' in row:
                stats['device_summary'][row['can_id_hex']] += 1
        
        # Error analysis
        error_count = 0
        if self.format_type == 'RS485_MODBUS':
            for row in self.data:
                if row.get('status') == 'ERROR':
                    error_count += 1
                    error_code = row.get('error_code', 'UNKNOWN')
                    stats['error_summary'][f'error_code_{error_code}'] = \
                        stats['error_summary'].get(f'error_code_{error_code}', 0) + 1
                
                # Value statistics by sensor type
                sensor_type = row.get('sensor_type', 'unknown')
                try:
                    value = float(row.get('value', 0))
                    if sensor_type not in stats['value_statistics']:
                        stats['value_statistics'][sensor_type] = {
                            'count': 0, 'sum': 0, 'min': float('inf'), 
                            'max': float('-inf'), 'values': []
                        }
                    
                    vstats = stats['value_statistics'][sensor_type]
                    vstats['count'] += 1
                    vstats['sum'] += value
                    vstats['min'] = min(vstats['min'], value)
                    vstats['max'] = max(vstats['max'], value)
                    vstats['values'].append(value)
                except (ValueError, TypeError):
                    pass
        
        elif self.format_type == 'CAN_BUS':
            for row in self.data:
                if row.get('bus_status') == 'ERROR' or row.get('error_frame') == '1':
                    error_count += 1
                    stats['error_summary']['error_frames'] = \
                        stats['error_summary'].get('error_frames', 0) + 1
                
                # Message type statistics
                msg_type = row.get('message_type', 'unknown')
                stats['value_statistics'][msg_type] = \
                    stats['value_statistics'].get(msg_type, 0) + 1
        
        # Calculate averages
        for sensor_type, vstats in stats['value_statistics'].items():
            if isinstance(vstats, dict) and 'count' in vstats and vstats['count'] > 0:
                vstats['avg'] = round(vstats['sum'] / vstats['count'], 2)
                vstats.pop('sum', None)
                # Keep only summary stats for JSON (remove raw values to save space)
                vstats.pop('values', None)
        
        stats['error_summary']['total_errors'] = error_count
        stats['error_summary']['error_rate'] = round(
            (error_count / len(self.data)) * 100, 2
        ) if len(self.data) > 0 else 0
        
        # Convert defaultdicts to regular dicts for JSON serialization
        stats['value_statistics'] = dict(stats['value_statistics'])
        stats['device_summary'] = dict(stats['device_summary'])
        stats['status_distribution'] = dict(stats['status_distribution'])
        
        self.statistics = stats
        return stats
    
    def generate_ascii_table(self, max_rows=20):
        """Generate ASCII table for terminal display"""
        if not self.data:
            return "No data available"
        
        lines = []
        lines.append("\n" + "="*80)
        lines.append(f"📊 DATA PREVIEW ({self.format_type}) - First {min(max_rows, len(self.data))} records")
        lines.append("="*80)
        
        # Table header
        headers = list(self.data[0].keys())[:6]  # Show first 6 columns
        header_line = " | ".join(f"{h[:15]:<15}" for h in headers)
        lines.append(header_line)
        lines.append("-" * len(header_line))
        
        # Table rows
        for i, row in enumerate(self.data[:max_rows]):
            values = [str(row.get(h, ''))[:15] for h in headers]
            line = " | ".join(f"{v:<15}" for v in values)
            lines.append(line)
        
        if len(self.data) > max_rows:
            lines.append(f"... and {len(self.data) - max_rows} more records")
        
        lines.append("="*80 + "\n")
        return "\n".join(lines)
    
    def generate_ascii_graph(self, metric='value', title="Data Distribution"):
        """Generate simple ASCII histogram"""
        if self.format_type != 'RS485_MODBUS':
            return "ASCII graphs currently supported for RS485/Modbus data only"
        
        # Group values by sensor type
        sensor_values = defaultdict(list)
        for row in self.data:
            try:
                sensor_type = row.get('sensor_type', 'unknown')
                value = float(row.get('value', 0))
                sensor_values[sensor_type].append(value)
            except (ValueError, TypeError):
                continue
        
        if not sensor_values:
            return "No valid numeric data for graphing"
        
        lines = []
        lines.append(f"\n📈 {title}")
        lines.append("="*70)
        
        for sensor_type, values in sorted(sensor_values.items()):
            if not values:
                continue
            
            avg = sum(values) / len(values)
            min_v = min(values)
            max_v = max(values)
            
            # Create bar visualization
            bar_length = int((avg / max_v) * 40) if max_v > 0 else 0
            bar = "█" * bar_length + "░" * (40 - bar_length)
            
            lines.append(f"{sensor_type:12} |{bar}| Avg: {avg:7.2f} | Min: {min_v:7.2f} | Max: {max_v:7.2f} | Count: {len(values):4}")
        
        lines.append("="*70 + "\n")
        return "\n".join(lines)
    
    def _generate_table_headers(self):
        """Generate HTML table headers"""
        if not self.data:
            return '<th>No data</th>'
        headers = list(self.data[0].keys())[:7]
        return ''.join(f'<th>{h}</th>' for h in headers)
    
    def _generate_table_rows(self):
        """Generate HTML table rows for first 10 records"""
        if not self.data:
            return '<tr><td colspan="7">No data available</td></tr>'
        
        rows = []
        for row in self.data[:10]:
            cells = ''.join(f'<td>{row.get(k, "")}</td>' for k in list(row.keys())[:7])
            rows.append(f'<tr>{cells}</tr>')
        return ''.join(rows)
    
    def generate_html_report(self, output_file='reports/data_analysis_report.html'):
        """Generate comprehensive HTML report with charts using Chart.js"""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Analysis Report - {self.format_type}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-card.error {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }}
        .stat-card.success {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }}
        .stat-value {{ font-size: 2em; font-weight: bold; }}
        .stat-label {{ font-size: 0.9em; opacity: 0.9; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #3498db; color: white; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .chart-container {{ position: relative; height: 400px; margin: 20px 0; }}
        .error-badge {{ background: #e74c3c; color: white; padding: 2px 8px; border-radius: 4px; }}
        .success-badge {{ background: #27ae60; color: white; padding: 2px 8px; border-radius: 4px; }}
        footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Data Analysis Report</h1>
        <p><strong>Format:</strong> {self.format_type} | <strong>Source:</strong> {self.input_file} | <strong>Generated:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h2>Executive Summary</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{self.statistics.get('total_records', 0)}</div>
                <div class="stat-label">Total Records</div>
            </div>
            <div class="stat-card {'error' if self.statistics.get('error_summary', {}).get('error_rate', 0) > 5 else 'success'}">
                <div class="stat-value">{self.statistics.get('error_summary', {}).get('error_rate', 0)}%</div>
                <div class="stat-label">Error Rate</div>
            </div>
            <div class="stat-card success">
                <div class="stat-value">{len(self.statistics.get('device_summary', {}))}</div>
                <div class="stat-label">Unique Devices/IDs</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(self.statistics.get('value_statistics', {}))}</div>
                <div class="stat-label">Sensor/Message Types</div>
            </div>
        </div>
        
        <h2>Status Distribution</h2>
        <div class="chart-container">
            <canvas id="statusChart"></canvas>
        </div>
        
        <h2>Device/ID Activity</h2>
        <div class="chart-container">
            <canvas id="deviceChart"></canvas>
        </div>
        
        <h2>Detailed Statistics</h2>
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Time Range</td>
                    <td>{self.statistics.get('time_range', {}).get('start', 'N/A')}</td>
                    <td>to {self.statistics.get('time_range', {}).get('end', 'N/A')}</td>
                </tr>
                <tr>
                    <td>Total Errors</td>
                    <td><span class="{'error-badge' if self.statistics.get('error_summary', {}).get('total_errors', 0) > 0 else 'success-badge'}">{self.statistics.get('error_summary', {}).get('total_errors', 0)}</span></td>
                    <td>Error codes: {list(self.statistics.get('error_summary', {}).keys())}</td>
                </tr>
            </tbody>
        </table>
        
        <h2>Data Preview (First 10 Records)</h2>
        <table>
            <thead>
                <tr>
                    {self._generate_table_headers()}
                </tr>
            </thead>
            <tbody>
                {self._generate_table_rows()}
            </tbody>
        </table>
        
        <footer>
            <p>Generated by Microcontroller-QWEN-Coder Data Analyzer | Internship Demo Project</p>
        </footer>
    </div>
    
    <script>
        // Status Distribution Chart
        const statusCtx = document.getElementById('statusChart').getContext('2d');
        new Chart(statusCtx, {{
            type: 'pie',
            data: {{
                labels: {json.dumps(list(self.statistics.get('status_distribution', {}).keys()))},
                datasets: [{{
                    data: {json.dumps(list(self.statistics.get('status_distribution', {}).values()))},
                    backgroundColor: ['#27ae60', '#e74c3c', '#f39c12', '#3498db', '#9b59b6']
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'bottom' }},
                    title: {{ display: true, text: 'Status Distribution' }}
                }}
            }}
        }});
        
        // Device Activity Chart
        const deviceCtx = document.getElementById('deviceChart').getContext('2d');
        new Chart(deviceCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(list(self.statistics.get('device_summary', {}).keys()))},
                datasets: [{{
                    label: 'Message Count',
                    data: {json.dumps(list(self.statistics.get('device_summary', {}).values()))},
                    backgroundColor: 'rgba(52, 152, 219, 0.7)',
                    borderColor: 'rgba(52, 152, 219, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{ beginAtZero: true }}
                }},
                plugins: {{
                    legend: {{ display: false }},
                    title: {{ display: true, text: 'Activity by Device/CAN ID' }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        print(f"✓ HTML report generated: {output_file}")
        return output_file
    
    def generate_json_report(self, output_file='reports/data_analysis.json'):
        """Generate JSON report with all statistics"""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(self.statistics, f, indent=2)
        
        print(f"✓ JSON report generated: {output_file}")
        return output_file
    
    def print_summary(self):
        """Print comprehensive summary to terminal"""
        print("\n" + "="*80)
        print("📋 ANALYSIS SUMMARY")
        print("="*80)
        print(f"Format: {self.statistics['format_type']}")
        print(f"Total Records: {self.statistics['total_records']}")
        print(f"Time Range: {self.statistics['time_range'].get('start', 'N/A')} to {self.statistics['time_range'].get('end', 'N/A')}")
        print(f"Error Rate: {self.statistics['error_summary'].get('error_rate', 0)}% ({self.statistics['error_summary'].get('total_errors', 0)} errors)")
        
        print("\n📦 Status Distribution:")
        for status, count in self.statistics['status_distribution'].items():
            percentage = (count / self.statistics['total_records']) * 100
            print(f"  • {status}: {count} ({percentage:.1f}%)")
        
        print("\n🔌 Device/ID Activity:")
        for device, count in sorted(self.statistics['device_summary'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  • {device}: {count} messages")
        
        if self.format_type == 'RS485_MODBUS':
            print("\n📊 Sensor Statistics:")
            for sensor_type, stats in self.statistics['value_statistics'].items():
                if isinstance(stats, dict) and 'avg' in stats:
                    print(f"  • {sensor_type}: Avg={stats['avg']}, Min={stats['min']:.2f}, Max={stats['max']:.2f}, Count={stats['count']}")
        
        print("="*80 + "\n")


def main():
    parser = argparse.ArgumentParser(description='Analyze serial monitor data from ESP32+RS485 or MCP2515 CAN projects')
    parser.add_argument('--input', '-i', required=True, help='Input CSV file from serial monitor')
    parser.add_argument('--output-dir', '-o', default='reports', help='Output directory for reports')
    parser.add_argument('--format', '-f', choices=['json', 'html', 'all', 'console'], default='all', help='Output format')
    parser.add_argument('--no-graph', action='store_true', help='Skip ASCII graph generation')
    
    args = parser.parse_args()
    
    try:
        # Initialize analyzer
        analyzer = DataAnalyzer(args.input)
        
        # Calculate statistics
        analyzer.calculate_statistics()
        
        # Print ASCII table preview
        print(analyzer.generate_ascii_table())
        
        # Print ASCII graph if enabled
        if not args.no_graph:
            print(analyzer.generate_ascii_graph())
        
        # Print summary
        analyzer.print_summary()
        
        # Generate reports
        os.makedirs(args.output_dir, exist_ok=True)
        
        if args.format in ['json', 'all']:
            json_file = os.path.join(args.output_dir, 'data_analysis.json')
            analyzer.generate_json_report(json_file)
        
        if args.format in ['html', 'all']:
            html_file = os.path.join(args.output_dir, 'data_analysis_report.html')
            analyzer.generate_html_report(html_file)
        
        print("\n✅ Analysis complete! Check the 'reports/' directory for detailed outputs.")
        print("💡 Tip: Open data_analysis_report.html in a browser for interactive charts.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
