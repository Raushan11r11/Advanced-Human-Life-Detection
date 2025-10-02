"""
Utility to save sensor data and features to CSV file.
"""

import csv
def save_to_csv(path, header, data):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
