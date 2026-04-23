# ESP32 RS485/MCP2515 Demo Data Generator
# Generates realistic sensor data simulating industrial IoT scenarios
# Output: CSV format compatible with serial monitor logs

import random
import csv
import datetime
import json
import os

def generate_esp32_rs485_data(num_records=100, output_file='data/demo_samples/esp32_rs485_demo.csv'):
    """
    Generate demo data simulating ESP32 reading sensors via RS485 (Modbus)
    Simulates: Temperature, Humidity, Pressure, Voltage, Current from multiple slave devices
    """
    print(f"Generating {num_records} RS485 sensor records...")
    
    headers = [
        'timestamp', 'device_id', 'sensor_type', 'value', 'unit', 
        'status', 'error_code', 'signal_quality', 'modbus_address'
    ]
    
    sensor_types = [
        ('temperature', '°C', -20, 85),
        ('humidity', '%RH', 0, 100),
        ('pressure', 'hPa', 900, 1100),
        ('voltage', 'V', 11, 14),
        ('current', 'A', 0, 20)
    ]
    
    device_ids = ['SLAVE_01', 'SLAVE_02', 'SLAVE_03', 'SLAVE_04']
    modbus_addresses = [1, 2, 3, 4]
    
    base_time = datetime.datetime.now()
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        for i in range(num_records):
            timestamp = base_time + datetime.timedelta(seconds=i*2)
            device_idx = random.randint(0, len(device_ids)-1)
            sensor_idx = random.randint(0, len(sensor_types)-1)
            
            sensor_name, unit, min_val, max_val = sensor_types[sensor_idx]
            
            # Generate realistic value with occasional anomalies
            if random.random() < 0.05:  # 5% chance of anomaly
                value = max_val * 1.2  # Over-range value
                status = 'ERROR'
                error_code = random.choice([1, 2, 3, 5])
                signal_quality = random.randint(20, 50)
            else:
                value = random.uniform(min_val, max_val)
                # Add some realistic variation patterns
                if sensor_name == 'temperature':
                    value += 5 * (i / num_records)  # Slight upward trend
                elif sensor_name == 'humidity':
                    value += 10 * (0.5 - random.random())  # Random fluctuation
                
                status = 'OK'
                error_code = 0
                signal_quality = random.randint(75, 100)
            
            row = [
                timestamp.isoformat(),
                device_ids[device_idx],
                sensor_name,
                round(value, 2),
                unit,
                status,
                error_code,
                signal_quality,
                modbus_addresses[device_idx]
            ]
            writer.writerow(row)
    
    print(f"✓ RS485 data saved to: {output_file}")
    return output_file


def generate_mcp2515_can_data(num_records=100, output_file='data/demo_samples/mcp2515_can_demo.csv'):
    """
    Generate demo data simulating MCP2515 CAN bus messages
    Simulates: Vehicle/Industrial CAN bus with various message IDs
    """
    print(f"Generating {num_records} CAN bus records...")
    
    headers = [
        'timestamp', 'can_id', 'can_id_hex', 'message_type', 'data_bytes',
        'dlc', 'priority', 'bus_status', 'error_frame'
    ]
    
    # Common CAN message types for automotive/industrial
    can_messages = [
        (0x100, 'ENGINE_RPM', [0, 0, 0, 0, 0, 0, 0, 0]),
        (0x200, 'VEHICLE_SPEED', [0, 0, 0, 0, 0, 0, 0, 0]),
        (0x300, 'BATTERY_VOLTAGE', [0, 0, 0, 0, 0, 0, 0, 0]),
        (0x400, 'MOTOR_TEMP', [0, 0, 0, 0, 0, 0, 0, 0]),
        (0x500, 'DIAGNOSTIC', [0, 0, 0, 0, 0, 0, 0, 0]),
        (0x600, 'CONTROL_CMD', [0, 0, 0, 0, 0, 0, 0, 0])
    ]
    
    base_time = datetime.datetime.now()
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        for i in range(num_records):
            timestamp = base_time + datetime.timedelta(milliseconds=i*50)
            msg_idx = random.randint(0, len(can_messages)-1)
            
            can_id, msg_type, _ = can_messages[msg_idx]
            can_id_hex = f"0x{can_id:03X}"
            
            # Generate realistic CAN data bytes
            dlc = random.choice([4, 5, 6, 8])  # Data Length Code
            data_bytes = []
            
            if msg_type == 'ENGINE_RPM':
                rpm = random.randint(800, 6000)
                data_bytes = [(rpm >> 8) & 0xFF, rpm & 0xFF] + [random.randint(0, 255) for _ in range(dlc-2)]
            elif msg_type == 'VEHICLE_SPEED':
                speed = random.randint(0, 180)
                data_bytes = [speed] + [random.randint(0, 255) for _ in range(dlc-1)]
            elif msg_type == 'BATTERY_VOLTAGE':
                voltage = random.randint(110, 150)  # Represented as 11.0-15.0V
                data_bytes = [voltage] + [random.randint(0, 255) for _ in range(dlc-1)]
            elif msg_type == 'MOTOR_TEMP':
                temp = random.randint(-40, 150)
                data_bytes = [temp + 40] + [random.randint(0, 255) for _ in range(dlc-1)]  # Offset encoding
            elif msg_type == 'DIAGNOSTIC':
                data_bytes = [random.randint(0, 255) for _ in range(dlc)]
            elif msg_type == 'CONTROL_CMD':
                data_bytes = [random.randint(0, 1), random.randint(0, 255)] + [random.randint(0, 255) for _ in range(dlc-2)]
            
            data_str = ' '.join(f"{b:02X}" for b in data_bytes[:dlc])
            
            # Occasional errors (2% chance)
            if random.random() < 0.02:
                bus_status = 'ERROR'
                error_frame = 1
            else:
                bus_status = 'OK'
                error_frame = 0
            
            priority = (can_id >> 5) & 0x07  # Extract priority from ID
            
            row = [
                timestamp.isoformat(),
                can_id,
                can_id_hex,
                msg_type,
                data_str,
                dlc,
                priority,
                bus_status,
                error_frame
            ]
            writer.writerow(row)
    
    print(f"✓ CAN bus data saved to: {output_file}")
    return output_file


def generate_combined_demo_data():
    """Generate both RS485 and CAN demo datasets"""
    rs485_file = generate_esp32_rs485_data(150)
    can_file = generate_mcp2515_can_data(150)
    
    # Create a summary JSON
    summary = {
        'generated_at': datetime.datetime.now().isoformat(),
        'datasets': [
            {
                'name': 'ESP32_RS485_Modbus',
                'file': rs485_file,
                'records': 150,
                'description': 'Simulated Modbus RTU sensor data over RS485'
            },
            {
                'name': 'MCP2515_CAN_Bus',
                'file': can_file,
                'records': 150,
                'description': 'Simulated CAN bus messages from vehicle/industrial system'
            }
        ],
        'usage_instructions': [
            'Use these files with: python tools/data_analyzer.py --input data/demo_samples/esp32_rs485_demo.csv',
            'Or for CAN data: python tools/data_analyzer.py --input data/demo_samples/mcp2515_can_demo.csv',
            'Files simulate real serial monitor output from PlatformIO projects'
        ]
    }
    
    summary_file = 'data/demo_samples/demo_summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✓ Demo summary saved to: {summary_file}")
    print("\n📊 Demo data generation complete!")
    print("   Files created:")
    print(f"   - {rs485_file}")
    print(f"   - {can_file}")
    print(f"   - {summary_file}")
    
    return summary


if __name__ == '__main__':
    generate_combined_demo_data()
