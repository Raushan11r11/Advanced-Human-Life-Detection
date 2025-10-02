# Advanced-Human-Life-Detection
A portable, real-time rescue tool that fuses mmWave radar, microphone, and accelerometer signals using advanced digital signal processing (FFT, DWT) and machine learning to detect survivors under debris.

## Features
- **Multi-sensor Fusion:** Integrates radar, audio, and vibration data.
- **Signal Processing:** DWT/FFT extraction for robust feature analysis.
- **Machine Learning:** Automatic detection using Random Forest/Custom ML model.
- **Real-time Feedback:** LCD, LED, and buzzer UI for instant alerts.
- **Data Logging:** Stores all measurements and predictions for research.

## Installation
1. Clone this repository:
    ```
    git clone https://github.com/yourusername/human-life-detection.git
    cd human-life-detection
    ```
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Connect Raspberry Pi and sensors (see `/config/config.py`).

## Usage
1. Prepare and connect your hardware.
2. Run:
    ```
    python main.py
    ```
3. View LCD, LED, and buzzer outputs for detection status.
4. Inspect and analyze sensor data in `ml/sensor_data.csv`.

## File Structure

| File/Folder         | Description                                  |
|---------------------|----------------------------------------------|
| `main.py`           | Main execution, ML prediction, plotting, UI  |
| `sensors/`          | Sensor interface classes for radar, mic, acc |
| `processing/`       | Signal processing (FFT, DWT), feature extract|
| `ui/`               | Hardware UI indicators (LCD, LED, buzzer)    |
| `config/`           | Hardware pin/address config                  |
| `utils/`            | Data saving utilities                        |
| `ml/model.pkl`      | Trained ML model (RandomForest, etc.)        |
| `ml/sensor_data.csv`| Collected sensor data                        |

## Contributing
Open issues or pull requests to improve hardware integration, add new signal processing features, or adapt model training.

## License
MIT

## Contact
For questions, open an issue or email `vijaysaravanan1609@gmail.com`.
