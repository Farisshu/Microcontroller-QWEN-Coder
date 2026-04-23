# Serial Data Analyzer Tool

## Overview
This tool analyzes serial monitor data from embedded systems projects (ESP32+RS485, MCP2515 CAN) and generates comprehensive reports with tables, statistics, and interactive charts.

## Features
- **Auto-detection** of RS485/Modbus and CAN bus data formats
- **ASCII tables** for terminal preview
- **ASCII histograms** for quick visualization
- **HTML reports** with interactive Chart.js graphs
- **JSON exports** for further processing
- **Error analysis** with error rate calculations
- **Device/ID activity tracking**
- **Sensor statistics** (min, max, avg, count)

## Quick Start

### 1. Generate Demo Data
```bash
# Generate sample RS485 and CAN bus data
make generate-data

# Or run directly
python tools/generate_demo_data.py
```

### 2. Analyze Data
```bash
# Analyze RS485 demo data
make analyze-data

# Analyze CAN bus demo data
make analyze-can

# Full workflow (generate + analyze)
make demo-full

# Analyze your own serial data
make analyze-custom FILE=path/to/your/serial_log.csv
```

## Usage Examples

### Command Line Interface

```bash
# Basic usage
python tools/data_analyzer.py -i data/demo_samples/esp32_rs485_demo.csv

# Specify output format (json, html, all, console)
python tools/data_analyzer.py -i data.csv -f html

# Skip ASCII graph generation
python tools/data_analyzer.py -i data.csv --no-graph

# Custom output directory
python tools/data_analyzer.py -i data.csv -o my_reports/
```

### From PlatformIO/VSCode Serial Monitor

1. **Export Serial Data**: Copy data from PlatformIO serial monitor
2. **Format as CSV**: Save with columns matching your protocol:
   - **RS485/Modbus**: `timestamp,device_id,sensor_type,value,unit,status,error_code`
   - **CAN Bus**: `timestamp,can_id,can_id_hex,message_type,data_bytes,dlc,bus_status`
3. **Run Analyzer**: 
   ```bash
   python tools/data_analyzer.py -i my_serial_data.csv -f all
   ```
4. **View Report**: Open `reports/data_analysis_report.html` in browser

## Data Format Examples

### RS485/Modbus CSV Format
```csv
timestamp,device_id,sensor_type,value,unit,status,error_code,signal_quality,modbus_address
2024-01-15T10:30:00,SLAVE_01,temperature,25.5,°C,OK,0,95,1
2024-01-15T10:30:02,SLAVE_02,humidity,65.2,%RH,OK,0,88,2
2024-01-15T10:30:04,SLAVE_01,voltage,12.3,V,ERROR,2,45,1
```

### CAN Bus CSV Format
```csv
timestamp,can_id,can_id_hex,message_type,data_bytes,dlc,priority,bus_status,error_frame
2024-01-15T10:30:00.100,256,0x100,ENGINE_RPM,1A 2B 3C 4D,4,2,OK,0
2024-01-15T10:30:00.150,512,0x200,VEHICLE_SPEED,45,1,3,OK,0
2024-01-15T10:30:00.200,768,0x300,BATTERY_VOLTAGE,7E 00 00 00,4,1,ERROR,1
```

## Output Files

### Generated Reports
- `reports/data_analysis.json` - Complete statistics in JSON format
- `reports/data_analysis_report.html` - Interactive HTML report with charts

### HTML Report Features
- Executive summary dashboard
- Status distribution pie chart
- Device/ID activity bar chart
- Detailed statistics table
- Data preview (first 10 records)
- Responsive design for mobile/desktop

## Internship Demo Workflow

```bash
# Step 1: Show CI/CD compliance
make check

# Step 2: Generate and analyze sensor data
make demo-full

# Step 3: Present HTML report
# Open reports/data_analysis_report.html in browser

# Step 4: Show MISRA compliance
cat docs/MISRA_Deviations.md
```

## Customization

### Adding New Data Formats
Edit `tools/data_analyzer.py` and add detection logic in `detect_format()`:

```python
def detect_format(self):
    headers = reader.fieldnames
    if 'your_custom_field' in headers:
        self.format_type = 'YOUR_FORMAT'
```

### Extending Statistics
Add custom calculations in `calculate_statistics()`:

```python
# Add your custom metric
stats['your_metric'] = self.calculate_your_metric()
```

## Troubleshooting

### "Unknown data format" Error
Ensure your CSV has the required columns:
- RS485: Must have `sensor_type` or `modbus_address`
- CAN: Must have `can_id` or `can_id_hex`

### Missing Charts in HTML Report
The HTML report uses Chart.js from CDN. Ensure you have internet access when opening the report.

### Large Data Files
For files >10,000 records:
- Use `--no-graph` to skip ASCII histogram
- Consider sampling your data first

## Integration with CI/CD

Add to your GitHub Actions workflow:

```yaml
- name: Analyze Serial Data
  run: |
    python tools/data_analyzer.py -i test_data/serial_output.csv -f json
    mv reports/data_analysis.json artifacts/serial_analysis.json

- name: Upload Analysis Results
  uses: actions/upload-artifact@v3
  with:
    name: data-analysis
    path: artifacts/serial_analysis.json
```

## Related Tools
- `scripts/cicd_checker.py` - CI/CD pipeline validation
- `scripts/generate_report.py` - Comprehensive report generation
- `tools/generate_demo_data.py` - Demo data generator

## License
MIT License - Part of Microcontroller-QWEN-Coder internship preparation project
