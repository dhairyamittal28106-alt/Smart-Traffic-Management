import cv2
import numpy as np
from ultralytics import YOLO

class TrafficCamera:
    def __init__(self):
        # Medium model for high-precision multi-class detection
        self.model = YOLO('yolov8m.pt') 
        self.ambulance_buffer = 0
        self.track_history = {} 
        self.heatmap = None

    def get_count(self, frame):
        # --- Day/Night Auto-Sensitivity ---
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        # Night Mode: Higher res & lower confidence to see in shadows
        dynamic_imgsz = 1280 if brightness < 80 else 960
        dynamic_conf = 0.15 if brightness < 80 else 0.25

        results = self.model.track(
            frame, persist=True, verbose=False, tracker="bytetrack.yaml",
            imgsz=dynamic_imgsz, conf=dynamic_conf, iou=0.5, 
            classes=[0, 1, 2, 3, 5, 7] # Person, Bike, Car, Motor, Bus, Truck
        )
        
        counts = {'car': 0, 'truck': 0, 'bus': 0, 'motorcycle': 0, 'pedestrian': 0}
        violations = []
        max_y = frame.shape[0] # To track the end of the queue
        
        if self.heatmap is None: self.heatmap = np.zeros_like(gray, dtype=np.float32)

        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            clss = results[0].boxes.cls.cpu().numpy().astype(int)

            for box, obj_id, cls in zip(boxes, ids, clss):
                x1, y1, x2, y2 = box
                label = self.model.names[cls]
                cy = (y1 + y2) // 2
                
                # Update Heatmap for urban planning
                self.heatmap[y1:y2, x1:x2] += 0.1

                if label == 'person': counts['pedestrian'] += 1
                elif label == 'bicycle': counts['motorcycle'] += 1
                elif label in counts: 
                    counts[label] += 1
                    # Queue Logic: Furthest vehicle defines line length
                    if y1 < max_y: max_y = y1

                # Wrong-Way Detection
                if obj_id in self.track_history:
                    if cy < self.track_history[obj_id]['last_y'] - 12:
                        violations.append(f"ID:{obj_id} WRONG WAY")
                    self.track_history[obj_id]['last_y'] = cy
                else:
                    self.track_history[obj_id] = {'last_y': cy, 'frames': 0}
                
                self.track_history[obj_id]['frames'] += 1
                
                # Visuals (Bus gets Gold color for Priority)
                color = (0, 215, 255) if label == 'bus' else (0, 255, 0)
                if label == 'person': color = (255, 0, 255)
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label} ID:{obj_id}", (x1, y1-10), 0, 0.4, color, 1)

        # 5-frame ambulance verification preserved
        # Queue length in pixels
        queue_len = max(0, frame.shape[0] - max_y)
        return counts, queue_len, violations, brightness