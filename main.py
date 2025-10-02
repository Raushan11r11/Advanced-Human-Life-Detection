import time
import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

from sensors.radar import RadarSensor
from sensors.microphone import MicrophoneSensor
from sensors.accelerometer import AccelerometerSensor
from processing.features import extract_features, feature_names
from ui.lcd import LCD
from ui.buzzer import Buzzer
from ui.led import LED
from utils.data import save_to_csv
from config.config import LCD_ADDRESS, LCD_PORT, BUZZER_PIN, LED_PIN1, LED_PIN2, LED_PIN3

# Load ML model
model = None
model_path = 'ml/model.pkl'
if os.path.exists(model_path):
    try:
        model = joblib.load(model_path)
        print("Loaded ML model for inference.")
    except Exception as e:
        print(f"Error loading ML model: {e}")
        print("Using rule-based detection.")
else:
    print("No trained model found. Using rule-based detection.")

# Initialize hardware
radar = RadarSensor()
mic = MicrophoneSensor()
acc = AccelerometerSensor()
lcd = LCD(address=LCD_ADDRESS, port=LCD_PORT)
buzzer = Buzzer(pin=BUZZER_PIN)
led = LED(pin1=LED_PIN1, pin2=LED_PIN2, pin3=LED_PIN3)

# For real-time plotting
plt.ion()
fig, axs = plt.subplots(4, 1, figsize=(12, 8))

timestamps, predictions = [], []
radar_presence, radar_distance = [], []
mic_peaks, acc_x_means = [], []
all_features = []

# LED status: Start
led.all_off()
led.on(1)
lcd.show_message("System Started", "Scanning...")

try:
    for i in range(20):
        t = time.time()
        radar_data = radar.read()
        mic_samples = mic.read()
        acc_x, acc_y, acc_z = acc.read()
        features = extract_features(radar_data, mic_samples, acc_x, acc_y, acc_z)

        if model:
            try:
                X_input = pd.DataFrame([features], columns=feature_names)
                prediction = int(model.predict(X_input))
            except Exception as e:
                print(f"Prediction error: {e}. Using rule-based.")
                prediction = int(radar_data['presence'] or features[2] > 120 or abs(features[5]) > 0.015)
        else:
            prediction = int(radar_data['presence'] or features[2] > 120 or abs(features[5]) > 0.015)

        # LED and LCD status
        if prediction:
            led.all_off()
            led.on(2)
            buzzer.alert(0.2)
            lcd.show_message("HUMAN DETECTED!", f"Move:{'Yes' if radar_data['presence'] else 'No'} Rng:{radar_data['distance_m']:.2f}")
        else:
            led.all_off()
            led.on(1)
            lcd.show_message("No Human Found", f"Move:{'Yes' if radar_data['presence'] else 'No'} Rng:{radar_data['distance_m']:.2f}")

        timestamps.append(t)
        predictions.append(prediction)
        radar_presence.append(radar_data['presence'])
        radar_distance.append(radar_data['distance_m'])
        mic_peaks.append(features[2])
        acc_x_means.append(features[5])
        all_features.append([t, prediction] + features)

        # Real-time plotting
        axs[0].clear()
        axs[0].plot(timestamps, predictions, 'r-', label='Detection')
        axs[0].set_ylabel('Detection')
        axs[0].legend()

        axs[1].clear()
        axs[1].plot(timestamps, radar_presence, 'b-', label='Radar')
        axs[1].set_ylabel('Radar')
        axs[1].legend()

        axs[2].clear()
        axs[2].plot(timestamps, mic_peaks, 'g-', label='Mic Peak')
        axs[2].set_ylabel('Mic Peak')
        axs[2].legend()

        axs[3].clear()
        axs[3].plot(timestamps, acc_x_means, 'm-', label='Acc X Mean')
        axs[3].set_ylabel('Acc X Mean')
        axs[3].set_xlabel('Time')
        axs[3].legend()

        plt.tight_layout()
        plt.pause(0.05)

        time.sleep(0.5)

    led.all_off()
    led.on(3)
    lcd.show_message("Process Complete", "20 cycles done")
finally:
    header = ['timestamp', 'detected'] + feature_names
    save_to_csv('ml/sensor_data.csv', header, all_features)
    plt.ioff()
    plt.show()
    led.all_off()
    lcd.show_message(" " * 16, " " * 16)
    GPIO.cleanup()
