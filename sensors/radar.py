"""
RadarSensor interface.
Reads motion presence and distance from radar hardware.
"""

class RadarSensor:
    def read(self):
        # Replace with hardware-specific code
        return {'presence': 1, 'distance_m': 1.23}  # Example dummy data
