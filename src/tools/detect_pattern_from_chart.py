import torch
import os
import cv2
from ultralyticsplus import YOLO
from langchain.tools import tool

# Patch for PyTorch 2.6+ to allow custom model loading
try:
    from ultralytics.nn.tasks import DetectionModel
    torch.serialization.add_safe_globals([DetectionModel])
except Exception:
    pass

@tool
def detect_pattern_from_chart(chart_path: str):
    """
    Loads a candlestick chart image and uses a YOLO model to detect trading patterns.
    Args:
    - candle_chart_path: Path to the candlestick chart PNG image.
    Returns:
    - Detected signal (BUY/SELL/HOLD) and confidence score.
    """

    # Patch torch.load to always use weights_only=False
    import types
    orig_torch_load = torch.load
    def patched_torch_load(*args, **kwargs):
        kwargs["weights_only"] = False
        return orig_torch_load(*args, **kwargs)
    torch.load = patched_torch_load

    model = YOLO("models/yolo/best.pt")
    model.overrides["iou"] = 0.45
    # model.overrides['agnostic_nms'] = False  # NMS class-agnostic
    # model.overrides['max_det'] = 1000  # maximum number of detections per image

    results = model.predict("src/dataset/candle_chart.png", conf=0.2)
    boxes = results[0].boxes

    # Restore original torch.load
    torch.load = orig_torch_load

    if len(boxes) == 0:
        print("No pattern detected")
        return None, None
    else:
        # Pick the rightmost box = most recent signal
        idx = torch.argmax(boxes.xyxy[:, 2]).item()
        label = model.names[int(boxes[idx].cls[0])]
        conf  = float(boxes[idx].conf[0])
        print(f"Signal: {label.upper()} | Confidence: {conf:.1%}")
        return {
            "trend": label.upper(),
            "conf_score": conf
        }