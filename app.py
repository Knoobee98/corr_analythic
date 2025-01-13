import pandas as pd
import matplotlib.pyplot as plt
import os

from tkinter import filedialog
# from google.colab import files

def process_csv_files(file_path):
  try:
    df = pd.read_csv(file_path)
    df['LinePoint'] = df['Line'].astype(str) + df['Point'].astype(str)
    df['TiltDegrees'] = df['Tilt degrees']
    battery = df[['LinePoint', 'BatteryVoltage mv', 'StartTime', 'posTime']]
    battery['StartTime'] = pd.to_datetime(battery['StartTime'])
    battery['posTime'] = pd.to_datetime(battery['posTime']).dt.tz_convert('UTC')
    battery['TimeDifference'] = (battery['posTime'] - battery['StartTime']).dt.total_seconds()
    tilt = df[['LinePoint', 'TiltDegrees']]

    # "Dropped Battery Event"
    voltage_threshold = 3400  # Example: 3000 mV

    dropped_voltage_events = battery[battery['BatteryVoltage mV'] < voltage_threshold]

    plt.figure(figsize=(12, 6))
    plt.scatter(dropped_voltage_events['TimeDifference'], dropped_voltage_events['BatteryVoltage mV'], color='red', label='Dropped Voltage')
    plt.scatter(battery['TimeDifference'], battery['BatteryVoltage mV'], color='blue', alpha=0.3, label='Normal Voltage') #Plot all data points for context

    plt.xlabel('Time Difference (seconds)')
    plt.ylabel('Battery Voltage (mV)')
    plt.title('Dropped Battery Voltage Events')
    plt.axhline(y=voltage_threshold, color='green', linestyle='--', label=f'Voltage Threshold ({voltage_threshold} mV)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # "Tilt Degrees Per Linepoint"
    tilt_mean = tilt.groupby('LinePoint')['TiltDegrees'].mean().head(50)

    plt.figure(figsize=(12, 6))
    plt.plot(tilt_mean.index, tilt_mean.values)
    plt.xlabel('LinePoint')
    plt.ylabel('Tilt Degrees')
    plt.title('Mean Tilt Degrees per LinePoint')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

  except FileNotFoundError:
    print(f"File Not Found: {file_path}")
    return None
  except Exception as e:
    print(f"An Error Occured While Processing {file_path} : {e}")
    return None

# directory = "./baaat/bet"  # Replace with the path to your directory	
# csv_files = [os.path.join(directory,file) for file in os.listdir(directory) if file.endswith('.csv')]

if __name__ == "__main__":
  file_path = filedialog.askopenfilename(
      title= "Select CSV File",
      filetypes= [("CSV Files"), "*.csv"]
  )

if file_path:
  processed_df = process_csv_files(file_path)
