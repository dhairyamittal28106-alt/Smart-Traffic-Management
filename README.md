# Smart Traffic Management

Computer-vision traffic prototype using YOLOv8 and ByteTrack to detect road users, adjust signal timing, estimate emissions, visualize a heatmap, and log metrics.

    python -m venv .venv
    pip install opencv-python numpy ultralytics
    python main.py

Run from the root. Opens traffic2.mp4 and appends to traffic_report.csv. Source includes main.py, vision_module.py, traffic_logic.py, and report_generator.py. Detection and emissions are estimates.
