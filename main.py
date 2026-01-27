import cv2
import numpy as np
import time
import csv
import os
from vision_module import TrafficCamera
from traffic_logic import TrafficBrain

cam = TrafficCamera()
brain = TrafficBrain()
cap = cv2.VideoCapture('traffic2.mp4')

# Initialize Data Log
report_file = 'traffic_report.csv'
if not os.path.exists(report_file):
    with open(report_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Load', 'Peds', 'CO2_g', 'Queue'])

current_timer = 0
last_time_check = time.time()
signal_status = "RED"

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    
    counts, queue, violations, brightness = cam.get_count(frame)
    total_load = counts['car'] + counts['truck'] + counts['bus'] + counts['motorcycle']
    co2 = brain.calculate_emissions(counts, signal_status)
    
    # UI: Blend Heatmap for visual analytics
    heatmap_norm = cv2.normalize(cam.heatmap, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    heatmap_color = cv2.applyColorMap(heatmap_norm, cv2.COLORMAP_JET)
    display_frame = cv2.resize(frame, (1280, 720)) 
    cv2.addWeighted(cv2.resize(heatmap_color, (1280, 720)), 0.3, display_frame, 0.7, 0, display_frame)

    now = time.time()
    dt = now - last_time_check
    last_time_check = now
    
    if current_timer > 0:
        current_timer -= dt
        signal_status = "GREEN"
    else:
        current_timer = 0
        signal_status = "RED"
        if total_load > 0 or counts['pedestrian'] > 0 or queue > 200:
            current_timer = brain.calculate_time(counts, queue)

    # Logging
    if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) % 30 == 0:
        with open(report_file, mode='a', newline='') as f:
            csv.writer(f).writerow([time.strftime("%H:%M:%S"), total_load, counts['pedestrian'], co2, queue])

    # --- ENHANCED HUD ---
    cv2.rectangle(display_frame, (0, 0), (1280, 80), (0, 0, 0), -1)
    
    # Status Panel
    overlay = display_frame.copy()
    cv2.rectangle(overlay, (20, 100), (320, 550), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, display_frame, 0.4, 0, display_frame)
    
    y = 140
    hud_color = (255, 255, 255) if brightness > 80 else (0, 255, 255)
    cv2.putText(display_frame, f"LIGHTING: {'DAY' if brightness > 80 else 'NIGHT'}", (40, y), 0, 0.6, hud_color, 1)
    for label, num in counts.items():
        y += 45
        cv2.putText(display_frame, f"{label.upper()}: {num}", (40, y), 0, 0.6, (0, 255, 255), 1)
    
    cv2.putText(display_frame, f"CO2: {co2:.1f}g/s", (40, y+50), 0, 0.7, (0, 255, 0), 2)
    
    # Violations in Red
    for i, v in enumerate(violations[:2]):
        cv2.putText(display_frame, f"ALERT: {v}", (40, y+100 + (i*30)), 0, 0.6, (0, 0, 255), 2)

    # Signal Light
    color = (0, 255, 0) if signal_status == "GREEN" else (0, 0, 255)
    cv2.circle(display_frame, (1150, 150), 55, color, -1)
    cv2.putText(display_frame, str(int(current_timer)), (1130, 165), 0, 1.2, (255, 255, 255), 3)

    cv2.imshow("Elite Smart Traffic AI Build", display_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()