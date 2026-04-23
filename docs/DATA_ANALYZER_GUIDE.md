# Serial Data Analyzer & Visualization Tools

## Overview
This toolkit provides automated analysis, visualization, and reporting for serial data collected from embedded systems (ESP32, RS485/Modbus, MCP2515 CAN bus). It transforms raw serial monitor output into professional reports with statistics, tables, and interactive charts.

## Features
- 📊 **Auto-Detection**: Automatically identifies RS485/Modbus or CAN bus data formats
- 📈 **Visualizations**: Generates HTML reports with interactive Chart.js graphs
- 📋 **Statistics**: Calculates min, max, average, standard deviation, and error rates
- 📑 **Tables**: Creates formatted ASCII and HTML data tables
- 🔍 **Error Analysis**: Detects anomalies, outliers, and communication errors
- 🚀 **CI/CD Integration**: Exports JSON reports for pipeline integration

## Prerequisites
```bash
# Install Python dependencies
pip install pandas matplotlib numpy jinja2
```

## Quick Start

### 1. Generate Demo Data
```bash
# Generate sample ESP32+RS485 data (150 records)
python tools/generate_demo_data.py --type rs485 --output data/demo_samples/esp32_rs485_demo.csv

# Generate sample MCP2515 CAN bus data (150 records)
python tools/generate_demo_data.py --type can --output data/demo_samples/mcp2515_can_demo.csv

# Generate both datasets
make generate-data
```

### 2. Analyze Your Data

#### Using Demo Data
```bash
# Analyze RS485 demo data
python tools/data_analyzer.py --input data/demo_samples/esp32_rs485_demo.csv --format rs485

# Analyze CAN bus demo data
python tools/data_analyzer.py --input data/demo_samples/mcp2515_can_demo.csv --format can

# Auto-detect format
python tools/data_analyzer.py --input data/demo_samples/esp32_rs485_demo.csv --auto
```

#### Using Your Own PlatformIO/VSCode Data
```bash
# Step 1: Copy serial monitor output to a text file
# Example format for RS485:
# timestamp,temperature,humidity,pressure,voltage,current
# 1704067200,25.3,60.2,1013.25,3.30,0.15
# 1704067201,25.4,60.1,1013.26,3.31,0.16

# Step 2: Run analyzer with auto-detection
python tools/data_analyzer.py --input your_serial_data.csv --auto

# Or specify format explicitly
python tools/data_analyzer.py --input your_serial_data.csv --format rs485
python tools/data_analyzer.py --input your_can_data.csv --format can
```

### 3. View Reports
```bash
# Open HTML report in browser
# Linux
xdg-open reports/data_analysis_report.html
# macOS
open reports/data_analysis_report.html
# Windows
start reports/data_analysis_report.html

# View JSON statistics
cat reports/data_analysis.json

# View ASCII summary in terminal
python tools/data_analyzer.py --input data/demo_samples/esp32_rs485_demo.csv --show-summary
```

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make generate-data` | Generate all demo datasets |
| `make analyze-data` | Analyze RS485 demo data |
| `make analyze-can` | Analyze CAN bus demo data |
| `make demo-full` | Complete workflow (generate + analyze + view) |
| `make analyze-custom FILE=<path>` | Analyze custom data file |
| `make clean-reports` | Remove generated reports |

### Examples
```bash
# Full demo workflow
make demo-full

# Analyze your custom data
make analyze-custom FILE=/path/to/your/serial_output.csv

# Clean up reports
make clean-reports
```

## Data Format Specifications

### RS485/Modbus Format (CSV)
```csv
timestamp,temperature,humidity,pressure,voltage,current,node_id
1704067200,25.3,60.2,1013.25,3.30,0.15,1
1704067201,25.4,60.1,1013.26,3.31,0.16,1
1704067202,25.5,59.9,1013.24,3.29,0.14,2
```

**Required Fields:**
- `timestamp`: Unix timestamp (seconds)
- At least one sensor field (temperature, humidity, pressure, voltage, current, etc.)

**Optional Fields:**
- `node_id`: Modbus slave address
- `error_code`: Communication error codes
- Custom sensor fields

### MCP2515 CAN Bus Format (CSV)
```csv
timestamp,can_id,rpm,speed_kmh,battery_voltage,motor_temp,throttle_position
1704067200,0x1A0,1500,45.2,12.6,35.5,25
1704067201,0x1A0,1550,46.1,12.7,36.0,27
1704067202,0x2B0,1600,47.5,12.5,37.2,30
```

**Required Fields:**
- `timestamp`: Unix timestamp (seconds)
- `can_id`: CAN message identifier (hex or decimal)
- At least one vehicle field (rpm, speed, voltage, temperature, etc.)

## Output Files

### Generated Reports
| File | Description |
|------|-------------|
| `reports/data_analysis_report.html` | Interactive HTML dashboard with charts |
| `reports/data_analysis.json` | Machine-readable statistics (CI/CD compatible) |
| `reports/data_table.txt` | ASCII-formatted data table |
| `reports/error_log.txt` | Detected anomalies and errors |

### JSON Report Structure
```json
{
  "metadata": {
    "source_file": "esp32_rs485_demo.csv",
    "format": "rs485",
    "record_count": 150,
    "analysis_timestamp": "2024-01-15T10:30:00Z"
  },
  "statistics": {
    "temperature": {
      "min": 22.1,
      "max": 28.7,
      "avg": 25.4,
      "std_dev": 1.23,
      "unit": "°C"
    }
  },
  "error_analysis": {
    "total_errors": 3,
    "error_rate_percent": 2.0,
    "anomalies": [...]
  },
  "charts_generated": ["temperature_trend", "humidity_distribution", ...]
}
```

## Integration with PlatformIO/VSCode

### Step 1: Export Serial Monitor Data
In VSCode with PlatformIO:
1. Open Serial Monitor (PlatformIO toolbar)
2. Click "Save Output" or copy data manually
3. Save as `serial_output.csv`

### Step 2: Format Data (if needed)
If your serial output is not CSV, use a simple script to convert:
```python
# Example: Convert "Temp: 25.3, Hum: 60.2" to CSV
import re
with open('raw_serial.txt', 'r') as f_in, open('formatted.csv', 'w') as f_out:
    f_out.write('timestamp,temperature,humidity\n')
    for line in f_in:
        match = re.search(r'Temp: ([\d.]+), Hum: ([\d.]+)', line)
        if match:
            f_out.write(f'{int(time.time())},{match.group(1)},{match.group(2)}\n')
```

### Step 3: Analyze
```bash
python tools/data_analyzer.py --input formatted.csv --auto
```

## Customization

### Add New Sensor Types
Edit `tools/data_analyzer.py`:
```python
CUSTOM_SENSORS = {
    'co2_level': {'unit': 'ppm', 'min_expected': 400, 'max_expected': 5000},
    'light_intensity': {'unit': 'lux', 'min_expected': 0, 'max_expected': 100000}
}
```

### Modify Chart Styles
Edit chart configuration in `tools/data_analyzer.py`:
```python
CHART_CONFIG = {
    'width': 1200,
    'height': 600,
    'colors': ['#3498db', '#e74c3c', '#2ecc71'],
    'theme': 'light'  # or 'dark'
}
```

## Troubleshooting

### Issue: "No valid data found"
**Solution**: Ensure your CSV has headers and at least one numeric data column.

### Issue: "Format detection failed"
**Solution**: Explicitly specify format with `--format rs485` or `--format can`.

### Issue: Charts not displaying in HTML
**Solution**: Ensure you have internet access to load Chart.js CDN, or download Chart.js locally.

### Issue: Memory error with large files
**Solution**: Use chunked processing:
```bash
python tools/data_analyzer.py --input large_file.csv --chunk-size 10000
```

## Example Workflow for Internship Demo

```bash
# 1. Generate realistic demo data
make generate-data

# 2. Analyze and create full report
make demo-full

# 3. Show live terminal output
python tools/data_analyzer.py --input data/demo_samples/esp32_rs485_demo.csv --show-summary

# 4. Open interactive HTML report
xdg-open reports/data_analysis_report.html

# 5. Export JSON for CI/CD pipeline
cat reports/data_analysis.json | jq '.statistics'
```

## Best Practices

1. **Timestamp Consistency**: Use Unix timestamps for easy analysis
2. **Data Validation**: Check for outliers before final presentation
3. **Report Versioning**: Include git commit hash in report metadata
4. **Error Documentation**: Log all detected anomalies for debugging
5. **Visualization Choice**: Use line charts for trends, bar charts for comparisons

## License
MIT License - See main repository LICENSE file

## Contributing
Add new sensor types, improve visualization options, or enhance error detection algorithms.
