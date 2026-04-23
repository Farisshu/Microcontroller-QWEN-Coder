# PDF Report Generator

A comprehensive tool for generating professional PDF reports from sensor data with full statistics, graphs, and analysis.

## Features

- **Full Data Analysis**: Automatically calculates comprehensive statistics including mean, median, standard deviation, min/max, variance, skewness, and kurtosis
- **Multiple Graph Types**: Generates 5 different visualization types:
  - Time Series Plot
  - Histogram with KDE overlay
  - Box Plot by Category
  - Status Distribution Pie Chart
  - Scatter Plot with correlation analysis
- **Professional Layout**: Landscape A4 format with styled tables and formatted text
- **Error Analysis**: Detailed breakdown of error codes and failure rates
- **Executive Summary**: Auto-generated summary with key findings
- **Recommendations**: Intelligent suggestions based on data analysis

## Installation

```bash
pip install reportlab pandas numpy matplotlib
```

## Usage

### Basic Usage

```bash
python tools/pdf_report_generator.py -i <input_csv> -o <output_pdf> [--title "Report Title"]
```

### Examples

```bash
# Generate report from RS485 demo data
python tools/pdf_report_generator.py -i data/demo_samples/esp32_rs485_demo.csv -o reports/rs485_analysis.pdf

# Generate report from CAN bus data
python tools/pdf_report_generator.py -i data/demo_samples/mcp2515_can_demo.csv -o reports/can_analysis.pdf --title "CAN Bus Analysis"

# Custom title
python tools/pdf_report_generator.py -i my_data.csv -o my_report.pdf --title "My Custom Sensor Report"
```

## Input CSV Format

The tool expects a CSV file with the following optional columns:

| Column | Description | Example |
|--------|-------------|---------|
| `timestamp` | Date/time of reading | 2024-01-15T10:30:00 |
| `device_id` | Device identifier | SLAVE_01 |
| `sensor_type` | Type of sensor | temperature |
| `value` | Measured value | 25.5 |
| `unit` | Unit of measurement | °C |
| `status` | Device status | OK/ERROR |
| `error_code` | Error code if any | 0 |
| `signal_quality` | Signal quality % | 95 |
| `modbus_address` | Modbus address | 1 |

**Note**: The tool works with partial data - only available columns are required.

## Output Report Contents

### 1. Title Page
- Report title
- Subtitle
- Generation timestamp
- Author

### 2. Executive Summary
- Overview of data analyzed
- Key metrics summary
- Main findings

### 3. Quick Metrics Table
- Total records
- Unique devices
- Sensor types count
- Error rate
- Success rate
- Average signal quality

### 4. Comprehensive Statistics
- Mean, median, std deviation
- Min, max, range
- Variance, skewness, kurtosis
- Signal quality stats
- Error statistics

### 5. Data Sample
- First 20 records displayed in table format

### 6. Visualizations (5 Graphs)
1. **Time Series**: Shows value trends over time
2. **Histogram**: Distribution of measured values with density curve
3. **Box Plot**: Comparison across sensor types
4. **Pie Chart**: Status distribution (OK vs ERROR)
5. **Scatter Plot**: Signal quality vs value correlation

### 7. Advanced Analytics
- Grouped statistics by sensor type
- Count, mean, std dev, min, max per category

### 8. Error Analysis
- Total errors count
- Error rate percentage
- Breakdown by error code

### 9. Conclusions
- System reliability assessment
- Signal quality evaluation
- Actionable recommendations

## Integration with Makefile

Add these targets to your Makefile:

```makefile
# Generate PDF report from CSV data
pdf-report:
python tools/pdf_report_generator.py \
-i data/demo_samples/esp32_rs485_demo.csv \
-o reports/sensor_analysis.pdf

# Full demo with data generation and PDF report
demo-pdf: generate-data pdf-report
@echo "✅ PDF report generated successfully!"
```

## Sample Output

Generated PDFs are saved to the `reports/` directory:
- `rs485_full_report.pdf` (~111KB) - Complete RS485 sensor analysis
- `can_bus_analysis.pdf` (~7KB) - CAN bus data analysis
- `demo_analysis.pdf` (~109KB) - Demo dataset analysis

## Troubleshooting

### Issue: "Unknown format code 'f' for object of type 'str'"
**Solution**: Ensure numeric columns contain actual numbers, not strings. The tool now handles this automatically.

### Issue: Missing graphs in output
**Solution**: Check that required columns exist in your CSV:
- Time series: requires `timestamp` and `value`
- Box plot: requires `sensor_type` and `value`
- Pie chart: requires `status`
- Scatter plot: requires `signal_quality` and `value`

### Issue: Matplotlib warnings
**Solution**: These are deprecation warnings and don't affect functionality. Update matplotlib to latest version to remove them.

## Dependencies

- Python 3.8+
- pandas >= 1.3.0
- numpy >= 1.20.0
- matplotlib >= 3.5.0
- reportlab >= 3.6.0

## License

MIT License - Feel free to use and modify for your projects!
