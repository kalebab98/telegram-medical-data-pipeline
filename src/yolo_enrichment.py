import os
import csv
from ultralytics import YOLO
from glob import glob

IMAGE_ROOT = 'data/raw/telegram_images'
OUTPUT_CSV = 'yolo_detections.csv'
MODEL_NAME = 'yolov8n.pt'  # You can use yolov8n.pt (nano), yolov8s.pt (small), etc.

# Load YOLOv8 model
model = YOLO(MODEL_NAME)

def get_all_images():
    # Recursively find all images in the directory
    exts = ('*.jpg', '*.jpeg', '*.png')
    for root, dirs, files in os.walk(IMAGE_ROOT):
        for ext in exts:
            for img_path in glob(os.path.join(root, ext)):
                yield img_path

def extract_message_id(image_path):
    # Assumes filename is message_id.jpg or message_id.png
    fname = os.path.basename(image_path)
    msg_id = fname.split('.')[0]
    return msg_id

def main():
    results = []
    for img_path in get_all_images():
        msg_id = extract_message_id(img_path)
        try:
            yolo_results = model(img_path)
            for det in yolo_results[0].boxes:
                cls = yolo_results[0].names[int(det.cls)]
                conf = float(det.conf)
                results.append({
                    'message_id': msg_id,
                    'image_path': img_path,
                    'detected_object_class': cls,
                    'confidence_score': conf
                })
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
    # Write results to CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['message_id', 'image_path', 'detected_object_class', 'confidence_score'])
        writer.writeheader()
        writer.writerows(results)
    print(f"Detection results saved to {OUTPUT_CSV} ({len(results)} detections)")

if __name__ == '__main__':
    main() 