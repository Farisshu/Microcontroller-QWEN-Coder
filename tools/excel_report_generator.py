#!/usr/bin/env python3
"""
Professional Excel Report Generator
Generates a multi-sheet Excel report with statistics, formatted data, and embedded charts.
"""

import pandas as pd
import numpy as np
import argparse
import os
from datetime import datetime
import xlsxwriter

def generate_excel_report(input_file, output_file, title="Data Analysis Report"):
    """
    Generates a comprehensive Excel report with multiple sheets, statistics, and charts.
    """
    print(f"📊 Generating Excel Report: {output_file}")
    
    # Load Data
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    # Clean column names for safety
    df.columns = [str(c).strip().replace('\n', ' ') for c in df.columns]
    
    # Identify numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not numeric_cols:
        print("⚠️ No numeric columns found. Cannot generate statistics or graphs.")
        return

    # Create Excel Writer with XlsxWriter engine
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    workbook = writer.book
    
    # Define Formats
    fmt_title = workbook.add_format({'bold': True, 'font_size': 18, 'align': 'center', 'valign': 'vcenter'})
    fmt_subtitle = workbook.add_format({'bold': True, 'font_size': 14, 'font_color': '#2E75B6'})
    fmt_header = workbook.add_format({'bold': True, 'bg_color': '#D9E1F2', 'border': 1, 'align': 'center'})
    fmt_cell = workbook.add_format({'border': 1, 'num_format': '#,##0.00'})
    fmt_cell_int = workbook.add_format({'border': 1, 'num_format': '#,##0'})
    fmt_text = workbook.add_format({'border': 1})
    fmt_key = workbook.add_format({'bold': True, 'bg_color': '#F2F2F2', 'border': 1})
    
    # ============================================================
    # SHEET 1: Executive Summary & High-Level Stats
    # ============================================================
    sheet_name = "Executive Summary"
    ws_sum = workbook.add_worksheet(sheet_name)
    
    # Title
    ws_sum.merge_range('A1:D1', title, fmt_title)
    ws_sum.write('A2', f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fmt_subtitle)
    
    # Key Metrics Table
    metrics = [
        ["Total Records", len(df)],
        ["Numeric Columns", len(numeric_cols)],
        ["Categorical Columns", len(categorical_cols)],
        ["Date Range (if avail)", "N/A"] # Placeholder logic
    ]
    
    # Check for date-like column for range
    date_col = None
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            date_col = col
            break
    
    if date_col:
        try:
            min_date = df[date_col].min()
            max_date = df[date_col].max()
            metrics[3] = ["Date Range", f"{min_date} to {max_date}"]
        except:
            pass

    ws_sum.write('A4', "Metric", fmt_header)
    ws_sum.write('B4', "Value", fmt_header)
    
    for i, (key, val) in enumerate(metrics):
        row = i + 5
        ws_sum.write(row, 0, key, fmt_key)
        ws_sum.write(row, 1, val, fmt_cell_int if isinstance(val, int) else fmt_text)
    
    ws_sum.set_column('A:A', 25)
    ws_sum.set_column('B:B', 25)

    # ============================================================
    # SHEET 2: Detailed Statistics
    # ============================================================
    sheet_stats = "Statistics"
    ws_stat = workbook.add_worksheet(sheet_stats)
    
    ws_stat.write('A1', "Detailed Statistical Analysis", fmt_title)
    
    # Calculate stats
    stats_df = df[numeric_cols].describe().transpose()
    # Add extra stats
    stats_df['variance'] = df[numeric_cols].var()
    stats_df['skewness'] = df[numeric_cols].skew()
    stats_df['kurtosis'] = df[numeric_cols].kurtosis()
    
    # Write to Excel
    stats_df.to_excel(writer, sheet_name=sheet_stats, startrow=3, header=True, index=True)
    
    # Re-fetch worksheet to apply formatting
    ws_stat = writer.sheets[sheet_stats]
    
    # Format headers
    for col_num, value in enumerate(stats_df.columns.values):
        ws_stat.write(3, col_num + 1, value, fmt_header)
    for row_num, value in enumerate(stats_df.index.values):
        ws_stat.write(row_num + 4, 0, value, fmt_key)
        
    ws_stat.set_column('A:A', 15)
    for i in range(len(stats_df.columns) + 1):
        ws_stat.set_column(i + 1, i + 1, 12)

    # ============================================================
    # SHEET 3: Raw Data (Formatted)
    # ============================================================
    sheet_data = "Raw Data"
    df.to_excel(writer, sheet_name=sheet_data, index=False, startrow=1)
    ws_data = writer.sheets[sheet_data]
    
    ws_data.write('A1', "Full Dataset", fmt_subtitle)
    
    # Format headers
    for col_num, value in enumerate(df.columns.values):
        ws_data.write(1, col_num, value, fmt_header)
    
    # Auto-fit columns based on content (limited to first 100 rows for speed)
    for i, col in enumerate(df.columns):
        max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
        ws_data.set_column(i, i, min(max_len, 50)) # Cap width at 50

    # ============================================================
    # SHEET 4: Charts & Visualizations
    # ============================================================
    sheet_chart = "Visualizations"
    ws_chart = workbook.add_worksheet(sheet_chart)
    ws_chart.write('A1', "Data Visualizations", fmt_title)
    
    chart_row = 3
    
    # Helper to create charts
    def add_chart(ws, chart_type, title, categories, values, row_pos, col_pos=0):
        chart = workbook.add_chart({'type': chart_type})
        chart.add_series({
                    'name': title,
                    'categories': categories,
                    'values': values,
                })
        chart.set_title({'name': title})
        chart.set_legend({'position': 'bottom'})
        ws.insert_chart(row_pos, col_pos, chart, {'x_scale': 1.5, 'y_scale': 1.5})
        return 15 # Approx rows used

    # 1. Line Chart for first numeric column (Trend)
    if len(df) > 1:
        target_col = numeric_cols[0]
        col_letter = xlsxwriter.utility.xl_col_to_name(df.columns.get_loc(target_col))
        # We need to refer to cells in the Raw Data sheet
        # Format: ='Raw Data'!$A$2:$A$100
        cat_range = f"='{sheet_data}'!$A$2:$A${len(df)+1}"
        val_range = f"='{sheet_data}'!${col_letter}$2:${col_letter}${len(df)+1}"
        
        chart = workbook.add_chart({'type': 'line'})
        chart.add_series({
            'name': target_col,
            'categories': cat_range,
            'values': val_range,
            'line': {'color': '#2E75B6'}
        })
        chart.set_title({'name': f"Trend: {target_col}"})
        ws_chart.insert_chart(chart_row, 0, chart, {'x_scale': 1.8, 'y_scale': 1.8})
        ws_chart.write(chart_row, 10, "Trend analysis of the primary numeric variable over the dataset index.", fmt_text)
        chart_row += 15

    # 2. Bar Chart for Aggregated Data (if categorical exists)
    if categorical_cols:
        cat_col = categorical_cols[0]
        num_col = numeric_cols[0]
        
        # Aggregate data for chart
        agg_df = df.groupby(cat_col)[num_col].mean().reset_index().sort_values(by=num_col, ascending=False)
        agg_df.to_excel(writer, sheet_name=sheet_chart, startrow=chart_row+2, startcol=10, index=False, header=True)
        
        # Define ranges for the aggregated data just written
        # The data is at J{row}, K{row}
        start_r = chart_row + 3
        end_r = chart_row + 2 + len(agg_df)
        cat_range_agg = f"='{sheet_chart}'!$J${start_r}:$J${end_r}"
        val_range_agg = f"='{sheet_chart}'!$K${start_r}:$K${end_r}"
        
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': f"Average {num_col} by {cat_col}",
            'categories': cat_range_agg,
            'values': val_range_agg,
            'fill': {'color': '#70AD47'}
        })
        chart.set_title({'name': f"Average {num_col} per {cat_col}"})
        chart.set_x_axis({'name': cat_col})
        chart.set_y_axis({'name': f"Average {num_col}"})
        
        ws_chart.insert_chart(chart_row, 0, chart, {'x_scale': 1.5, 'y_scale': 1.5})
        ws_chart.write(chart_row, 8, f"Aggregated View: Mean of '{num_col}' grouped by '{cat_col}'", fmt_subtitle)
        chart_row += 15

    # 3. Histogram (Simulated via bins in a new helper sheet or simple bar of counts)
    # Let's create a frequency table for the first numeric column
    target_hist = numeric_cols[0]
    counts, bins = np.histogram(df[target_hist].dropna(), bins=10)
    hist_df = pd.DataFrame({
        'Bin': [f"{bins[i]:.1f}-{bins[i+1]:.1f}" for i in range(len(counts))],
        'Frequency': counts
    })
    
    hist_sheet = "Hist_Data"
    hist_df.to_excel(writer, sheet_name=hist_sheet, index=False)
    ws_hist = writer.sheets[hist_sheet]
    
    h_cat_range = f"='{hist_sheet}'!$A$2:$A${len(hist_df)+1}"
    h_val_range = f"='{hist_sheet}'!$B$2:$B${len(hist_df)+1}"
    
    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({
        'name': 'Distribution',
        'categories': h_cat_range,
        'values': h_val_range,
        'fill': {'color': '#FFC000'}
    })
    chart.set_title({'name': f"Distribution (Histogram) of {target_hist}"})
    chart.set_x_axis({'name': 'Range'})
    chart.set_y_axis({'name': 'Count'})
    
    ws_chart.insert_chart(chart_row, 0, chart, {'x_scale': 1.5, 'y_scale': 1.5})
    ws_chart.write(chart_row, 8, f"Frequency distribution showing how values of '{target_hist}' are spread.", fmt_subtitle)

    # Close and save
    writer.close()
    print(f"✅ Report successfully generated: {output_file}")
    print(f"   - Sheets: {', '.join([sheet_name, sheet_stats, sheet_data, sheet_chart, hist_sheet])}")

def main():
    parser = argparse.ArgumentParser(description="Generate Professional Excel Report")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file")
    parser.add_argument("-o", "--output", default="report.xlsx", help="Output Excel file")
    parser.add_argument("-t", "--title", default="Data Analysis Report", help="Report Title")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"❌ File not found: {args.input}")
        return
        
    generate_excel_report(args.input, args.output, args.title)

if __name__ == "__main__":
    main()
