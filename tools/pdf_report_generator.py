#!/usr/bin/env python3
"""
PDF Report Generator with Statistics and Graphs
Generates comprehensive PDF reports from sensor data with charts, statistics, and analysis.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from io import BytesIO

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


class PDFReportGenerator:
    """Generate comprehensive PDF reports with data, statistics, and graphs."""
    
    def __init__(self, output_path: str, title: str = "Data Analysis Report"):
        self.output_path = output_path
        self.title = title
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=landscape(A4),
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        self.styles = getSampleStyleSheet()
        self.elements = []
        self._setup_styles()
        
    def _setup_styles(self):
        """Configure custom styles for the report."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.darkblue,
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.darkblue,
            spaceBefore=20,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.darkslategray,
            spaceBefore=12,
            spaceAfter=8,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='NormalJustify',
            parent=self.styles['Normal'],
            alignment=TA_JUSTIFY,
            fontSize=10
        ))
        
        self.styles.add(ParagraphStyle(
            name='DataTableStyle',
            parent=self.styles['Normal'],
            fontSize=8,
            fontName='Helvetica'
        ))
        
    def add_title_page(self, subtitle: str = "", author: str = ""):
        """Add a title page to the report."""
        title = Paragraph(self.title, self.styles['CustomTitle'])
        self.elements.append(title)
        self.elements.append(Spacer(1, 0.3*inch))
        
        if subtitle:
            sub = Paragraph(subtitle, self.styles['Heading3'])
            self.elements.append(sub)
            self.elements.append(Spacer(1, 0.2*inch))
            
        timestamp = Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['Normal']
        )
        self.elements.append(timestamp)
        
        if author:
            self.elements.append(Spacer(1, 0.3*inch))
            auth = Paragraph(f"Author: {author}", self.styles['Normal'])
            self.elements.append(auth)
            
        self.elements.append(PageBreak())
        
    def add_section_header(self, text: str):
        """Add a section header."""
        header = Paragraph(text, self.styles['SectionHeader'])
        self.elements.append(header)
        
    def add_subsection_header(self, text: str):
        """Add a subsection header."""
        header = Paragraph(text, self.styles['SubsectionHeader'])
        self.elements.append(header)
        
    def add_text(self, text: str, style_name: str = 'NormalJustify'):
        """Add a paragraph of text."""
        style = self.styles[style_name]
        para = Paragraph(text, style)
        self.elements.append(para)
        
    def add_spacer(self, height: float = 0.2):
        """Add vertical space."""
        self.elements.append(Spacer(1, height*inch))
        
    def create_plot_image(self, fig: Figure) -> bytes:
        """Convert matplotlib figure to image bytes."""
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        return buf.getvalue()
    
    def add_graph(self, fig: Figure, caption: str = "", width: float = 6.5):
        """Add a graph/image to the report."""
        img_data = self.create_plot_image(fig)
        temp_path = "/tmp/temp_plot.png"
        with open(temp_path, 'wb') as f:
            f.write(img_data)
            
        img = Image(temp_path, width=width*inch, height=width*inch*0.6)
        self.elements.append(img)
        
        if caption:
            self.elements.append(Spacer(1, 0.1*inch))
            cap = Paragraph(f"<i>{caption}</i>", self.styles['Normal'])
            self.elements.append(cap)
            
        self.elements.append(Spacer(1, 0.2*inch))
        plt.close(fig)
        
    def add_statistics_table(self, stats: dict, title: str = "Statistics Summary"):
        """Add a statistics table."""
        self.add_subsection_header(title)
        
        data = [["Metric", "Value"]]
        for key, value in stats.items():
            if isinstance(value, float):
                data.append([key.replace('_', ' ').title(), f"{value:.4f}"])
            else:
                data.append([key.replace('_', ' ').title(), str(value)])
                
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        self.elements.append(table)
        self.elements.append(Spacer(1, 0.3*inch))
        
    def add_data_table(self, df: pd.DataFrame, title: str = "Data Sample", max_rows: int = 20):
        """Add a data sample table."""
        self.add_subsection_header(title)
        
        # Limit rows for readability
        display_df = df.head(max_rows)
        
        # Convert to list of lists
        data = [df.columns.tolist()] + display_df.values.tolist()
        
        # Truncate long values
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                if isinstance(val, str) and len(val) > 30:
                    data[i][j] = val[:27] + "..."
                elif isinstance(val, float):
                    data[i][j] = f"{val:.2f}"
                    
        # Calculate column widths
        num_cols = len(data[0])
        col_widths = [2.5*inch] + [(6.5*inch - 2.5*inch) / (num_cols - 1)] * (num_cols - 1)
        
        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkslategray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        self.elements.append(table)
        self.elements.append(Spacer(1, 0.2*inch))
        
        if len(df) > max_rows:
            note = Paragraph(f"<i>Showing first {max_rows} of {len(df)} records</i>", self.styles['Normal'])
            self.elements.append(note)
            
        self.elements.append(Spacer(1, 0.3*inch))
        
    def generate(self):
        """Build the PDF document."""
        self.doc.build(self.elements)
        print(f"✓ PDF report generated: {self.output_path}")


def create_time_series_plot(df: pd.DataFrame, value_col: str = 'value', 
                           title: str = "Time Series Analysis") -> Figure:
    """Create a time series plot."""
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Convert timestamp if needed
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        ax.plot(df['timestamp'], df[value_col], linewidth=0.8, marker='', color='steelblue')
        ax.set_xlabel('Timestamp')
    else:
        ax.plot(df.index, df[value_col], linewidth=0.8, color='steelblue')
        ax.set_xlabel('Sample Index')
        
    ax.set_ylabel(value_col.title())
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig


def create_histogram_plot(df: pd.DataFrame, value_col: str = 'value',
                         title: str = "Distribution Analysis") -> Figure:
    """Create a histogram with KDE."""
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Histogram
    ax.hist(df[value_col].dropna(), bins=30, alpha=0.7, color='coral', 
            edgecolor='black', label='Frequency', density=False)
    
    # KDE overlay
    df[value_col].dropna().plot(kind='density', ax=ax, color='darkred', 
                                 linewidth=2, label='Density')
    
    ax.set_xlabel(value_col.title())
    ax.set_ylabel('Frequency / Density')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return fig


def create_box_plot(df: pd.DataFrame, group_col: str = 'sensor_type', 
                   value_col: str = 'value', title: str = "Box Plot by Category") -> Figure:
    """Create a box plot grouped by category."""
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Get unique groups
    groups = df[group_col].unique()
    
    # Prepare data for boxplot
    data = [df[df[group_col] == g][value_col].dropna().values for g in sorted(groups)]
    labels = sorted(groups)
    
    bp = ax.boxplot(data, labels=labels, patch_artist=True, notch=True)
    
    # Color the boxes
    colors_list = plt.cm.Set3(np.linspace(0, 1, len(data)))
    for patch, color in zip(bp['boxes'], colors_list):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_xlabel(group_col.replace('_', ' ').title())
    ax.set_ylabel(value_col.title())
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig


def create_status_pie_chart(df: pd.DataFrame, status_col: str = 'status',
                           title: str = "Status Distribution") -> Figure:
    """Create a pie chart for status distribution."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    status_counts = df[status_col].value_counts()
    
    colors_list = plt.cm.Set2(np.linspace(0, 1, len(status_counts)))
    
    wedges, texts, autotexts = ax.pie(
        status_counts.values, 
        labels=status_counts.index,
        autopct='%1.1f%%',
        colors=colors_list,
        startangle=90,
        explode=[0.05] * len(status_counts)
    )
    
    # Enhance text visibility
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')
    
    ax.set_title(title, fontsize=12, fontweight='bold')
    plt.tight_layout()
    
    return fig


def create_scatter_plot(df: pd.DataFrame, x_col: str = 'signal_quality', 
                       y_col: str = 'value', title: str = "Scatter Analysis") -> Figure:
    """Create a scatter plot."""
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Color by status if available
    if 'status' in df.columns:
        status_colors = {'OK': 'green', 'ERROR': 'red', 'WARNING': 'orange'}
        colors = [status_colors.get(s, 'blue') for s in df['status']]
        scatter = ax.scatter(df[x_col], df[y_col], c=colors, alpha=0.6, s=30)
        
        # Create legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor='green', markersize=8, label='OK'),
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor='red', markersize=8, label='ERROR'),
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor='blue', markersize=8, label='Other')
        ]
        ax.legend(handles=legend_elements, loc='best')
    else:
        ax.scatter(df[x_col], df[y_col], alpha=0.6, s=30, color='steelblue')
    
    ax.set_xlabel(x_col.replace('_', ' ').title())
    ax.set_ylabel(y_col.title())
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return fig


def calculate_comprehensive_statistics(df: pd.DataFrame) -> dict:
    """Calculate comprehensive statistics for numeric columns."""
    stats = {}
    
    # Basic info
    stats['total_records'] = len(df)
    stats['numeric_columns'] = len(df.select_dtypes(include=[np.number]).columns)
    
    # For main value column
    value_cols = ['value', 'temperature', 'humidity', 'pressure', 'voltage', 'current']
    value_col = None
    for col in value_cols:
        if col in df.columns:
            value_col = col
            break
    
    if value_col and value_col in df.columns:
        series = df[value_col].dropna()
        if len(series) > 0 and pd.api.types.is_numeric_dtype(series):
            stats[f'{value_col}_mean'] = float(series.mean())
            stats[f'{value_col}_median'] = float(series.median())
            stats[f'{value_col}_std'] = float(series.std())
            stats[f'{value_col}_min'] = float(series.min())
            stats[f'{value_col}_max'] = float(series.max())
            stats[f'{value_col}_range'] = float(series.max() - series.min())
            stats[f'{value_col}_variance'] = float(series.var())
            stats[f'{value_col}_skewness'] = float(series.skew())
            stats[f'{value_col}_kurtosis'] = float(series.kurtosis())
        
    # Signal quality stats
    if 'signal_quality' in df.columns:
        sq = df['signal_quality'].dropna()
        if len(sq) > 0 and pd.api.types.is_numeric_dtype(sq):
            stats['signal_quality_avg'] = float(sq.mean())
            stats['signal_quality_min'] = float(sq.min())
            stats['signal_quality_max'] = float(sq.max())
        
    # Error rate
    if 'status' in df.columns:
        total = len(df)
        errors = len(df[df['status'] == 'ERROR'])
        stats['error_count'] = errors
        stats['error_rate_percent'] = float(errors / total * 100) if total > 0 else 0.0
        stats['success_rate_percent'] = float(100 - stats['error_rate_percent'])
        
    # Device count
    if 'device_id' in df.columns:
        stats['unique_devices'] = df['device_id'].nunique()
        
    # Sensor type count
    if 'sensor_type' in df.columns:
        stats['unique_sensor_types'] = df['sensor_type'].nunique()
        
    return stats


def generate_pdf_report(input_file: str, output_file: str, title: str = "Comprehensive Data Analysis Report"):
    """Generate a complete PDF report from CSV data."""
    
    # Load data
    print(f"📊 Loading data from: {input_file}")
    df = pd.read_csv(input_file)
    print(f"✓ Loaded {len(df)} records with {len(df.columns)} columns")
    
    # Initialize report
    reporter = PDFReportGenerator(output_file, title=title)
    
    # Title page
    reporter.add_title_page(
        subtitle="Statistical Analysis & Visualization Report",
        author="Automated Report Generator"
    )
    
    # Executive Summary
    reporter.add_section_header("Executive Summary")
    stats = calculate_comprehensive_statistics(df)
    
    signal_quality_avg = stats.get('signal_quality_avg', 0)
    error_rate = stats.get('error_rate_percent', 0)
    
    summary_text = f"""
    This report presents a comprehensive analysis of {stats['total_records']} sensor data records 
    collected from {stats.get('unique_devices', 'N/A')} devices. The dataset contains 
    {stats['numeric_columns']} numeric columns with various measurements including temperature, 
    humidity, pressure, voltage, and current readings. 
    
    Key findings include an average signal quality of {signal_quality_avg:.2f}% 
    and an error rate of {error_rate:.2f}%. The following sections provide 
    detailed statistical analysis and visualizations of the collected data.
    """
    reporter.add_text(summary_text)
    reporter.add_spacer(0.3)
    
    # Quick Stats Table
    reporter.add_subsection_header("Key Metrics Overview")
    quick_stats = {
        'Total Records': str(stats['total_records']),
        'Unique Devices': str(stats.get('unique_devices', 'N/A')),
        'Sensor Types': str(stats.get('unique_sensor_types', 'N/A')),
        'Error Rate (%)': f"{stats.get('error_rate_percent', 0):.2f}",
        'Success Rate (%)': f"{stats.get('success_rate_percent', 100):.2f}",
        'Avg Signal Quality': f"{stats.get('signal_quality_avg', 0):.2f}%"
    }
    reporter.add_statistics_table(quick_stats, "Quick Metrics")
    
    # Detailed Statistics
    reporter.add_section_header("Detailed Statistical Analysis")
    reporter.add_statistics_table(stats, "Comprehensive Statistics")
    
    # Data Sample
    reporter.add_section_header("Data Sample")
    reporter.add_data_table(df, "First 20 Records", max_rows=20)
    
    # Visualizations
    reporter.add_section_header("Data Visualizations")
    
    # Time Series Plot
    if 'timestamp' in df.columns and 'value' in df.columns:
        fig = create_time_series_plot(df, 'value', "Time Series Analysis of Sensor Values")
        reporter.add_graph(fig, "Figure 1: Time series showing sensor value trends over time")
    
    # Histogram
    if 'value' in df.columns:
        fig = create_histogram_plot(df, 'value', "Distribution of Sensor Values")
        reporter.add_graph(fig, "Figure 2: Histogram showing the frequency distribution of measured values")
    
    # Box Plot by Sensor Type
    if 'sensor_type' in df.columns and 'value' in df.columns:
        fig = create_box_plot(df, 'sensor_type', 'value', "Sensor Value Distribution by Type")
        reporter.add_graph(fig, "Figure 3: Box plot comparing value distributions across different sensor types")
    
    # Status Pie Chart
    if 'status' in df.columns:
        fig = create_status_pie_chart(df, 'status', "Operational Status Distribution")
        reporter.add_graph(fig, "Figure 4: Pie chart showing the proportion of OK vs ERROR states")
    
    # Scatter Plot
    if 'signal_quality' in df.columns and 'value' in df.columns:
        fig = create_scatter_plot(df, 'signal_quality', 'value', "Signal Quality vs Sensor Value")
        reporter.add_graph(fig, "Figure 5: Scatter plot correlating signal quality with measured values")
    
    # Additional Analysis Section
    reporter.add_section_header("Advanced Analytics")
    
    # Group by sensor type statistics
    if 'sensor_type' in df.columns and 'value' in df.columns:
        reporter.add_subsection_header("Statistics by Sensor Type")
        group_stats = df.groupby('sensor_type')['value'].agg(['count', 'mean', 'std', 'min', 'max'])
        group_stats = group_stats.round(4)
        
        data = [["Sensor Type", "Count", "Mean", "Std Dev", "Min", "Max"]]
        for idx, row in group_stats.iterrows():
            data.append([
                str(idx),
                int(row['count']),
                f"{row['mean']:.4f}",
                f"{row['std']:.4f}",
                f"{row['min']:.4f}",
                f"{row['max']:.4f}"
            ])
            
        table = Table(data, colWidths=[1.2*inch, 0.8*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        reporter.elements.append(table)
        reporter.add_spacer(0.3)
    
    # Error Analysis
    if 'status' in df.columns:
        reporter.add_subsection_header("Error Analysis")
        error_df = df[df['status'] == 'ERROR']
        error_stats = {
            'Total Errors': len(error_df),
            'Error Rate (%)': f"{stats.get('error_rate_percent', 0):.2f}",
        }
        
        if 'error_code' in error_df.columns:
            error_codes = error_df['error_code'].value_counts()
            for i, (code, count) in enumerate(error_codes.items()):
                error_stats[f'Error Code {code} Count'] = count
                
        reporter.add_statistics_table(error_stats, "Error Statistics")
    
    # Conclusions
    reporter.add_section_header("Conclusions")
    conclusion_text = f"""
    Based on the analysis of {stats['total_records']} data points, the system demonstrates 
    {stats.get('success_rate_percent', 100):.1f}% operational reliability. The average signal 
    quality of {stats.get('signal_quality_avg', 0):.1f}% indicates {'good' if stats.get('signal_quality_avg', 0) > 80 else 'moderate'} 
    communication stability.
    
    {'The error rate of ' + str(round(stats.get('error_rate_percent', 0), 2)) + '% suggests ' + 
     ('excellent system health.' if stats.get('error_rate_percent', 0) < 5 else 
      'room for improvement in system reliability.' if stats.get('error_rate_percent', 0) < 20 else
      'significant issues requiring attention.') if 'error_rate_percent' in stats else ''}
    
    Recommendations:
    • Continue monitoring signal quality trends
    • Investigate recurring error patterns
    • Implement predictive maintenance based on observed trends
    • Review device configurations for optimal performance
    """
    reporter.add_text(conclusion_text)
    
    # Generate the PDF
    reporter.generate()
    
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Generate comprehensive PDF reports with statistics and graphs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i data/demo_samples/esp32_rs485_demo.csv -o reports/analysis.pdf
  %(prog)s -i data.csv -o report.pdf --title "My Custom Report"
        """
    )
    
    parser.add_argument('-i', '--input', required=True, help='Input CSV file')
    parser.add_argument('-o', '--output', required=True, help='Output PDF file')
    parser.add_argument('--title', default='Comprehensive Data Analysis Report',
                       help='Report title (default: Comprehensive Data Analysis Report)')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    try:
        generate_pdf_report(args.input, args.output, args.title)
        print(f"\n✅ Report successfully generated: {args.output}")
        print(f"📄 Open the PDF to view statistics, graphs, and analysis!")
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
