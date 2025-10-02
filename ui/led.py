"""
LED control for status indication (started, human detected, completed).
"""

class LED:
    def __init__(self, pin1, pin2, pin3):
        pass
    def on(self, led_num):
        print(f"LED {led_num} ON")
    def all_off(self):
        print("All LEDs OFF")
