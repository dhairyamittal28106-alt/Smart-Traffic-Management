# Smart Traffic Management

A video-based traffic-monitoring prototype using YOLOv8 and ByteTrack. It detects and tracks pedestrians and vehicles, adjusts signal timing using observed demand, estimates idle emissions, renders a heatmap/status overlay, and logs measurements to CSV.

## Requirements and run

Use Python 3.10 or newer:

    python -m venv .venv
    # Activate the environment, then:
    pip install opencv-python numpy ultralytics
    python main.py

Run from the repository root. The current entry point reads `traffic2.mp4`, loops the video, displays the analysis window, and appends metrics to `traffic_report.csv`. Close the window to stop it. YOLO weights and sample videos are included.

## Source files

- `main.py`: video loop, signal state, display, and CSV logging
- `vision_module.py`: detection, tracking, and heatmap updates
- `traffic_logic.py`: timing and emissions heuristics
- `report_generator.py`: report generation helpers

This is a prototype: detection performance and emissions values depend on the input footage, model, and simplifying assumptions.
