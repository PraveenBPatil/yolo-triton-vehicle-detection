
import cv2
import numpy as np
import time
import tritonclient.http as httpclient
from pymongo import MongoClient
from datetime import datetime, timezone
from ultralytics.engine.results import Boxes
from ultralytics.trackers.byte_tracker import BYTETracker
from types import SimpleNamespace
from multiprocessing import Process, Queue


# Database worker: receives records through IPC and saves them
def database_worker(queue):
    mongo_client = MongoClient("mongodb://localhost:27017/")
    collection = mongo_client["traffic_db"]["detections"]

    try:
        while True:
            detection = queue.get()

            if detection is None:
                break

            collection.insert_one(detection)
            print("Saved car ID:", detection["car_id"])

    finally:
        mongo_client.close()


def main():
    # Connect to Triton
    client = httpclient.InferenceServerClient("localhost:8000")

    # Start database worker process
    detection_queue = Queue()
    db_process = Process(
        target=database_worker,
        args=(detection_queue,)
    )
    db_process.start()

    cap = None
    saved_count = 0

    try:
        cap = cv2.VideoCapture("vehicle moving.mp4")

        if not cap.isOpened():
            raise FileNotFoundError("Cannot open vehicle moving.mp4")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_time = 1 / fps if fps > 0 else 1 / 30

        # Initialize car tracker
        tracker = BYTETracker(SimpleNamespace(
            track_high_thresh=0.40,
            track_low_thresh=0.10,
            new_track_thresh=0.40,
            track_buffer=30,
            match_thresh=0.80,
            fuse_score=True
        ))

        while True:
            start = time.perf_counter()

            ret, frame = cap.read()
            if not ret:
                break

            h, w = frame.shape[:2]

            # Resize while preserving aspect ratio
            scale = min(640 / w, 640 / h)
            nw, nh = int(w * scale), int(h * scale)
            resized = cv2.resize(frame, (nw, nh))

            # Add padding to create a 640x640 image
            image = np.full((640, 640, 3), 114, dtype=np.uint8)
            left, top = (640 - nw) // 2, (640 - nh) // 2
            image[top:top + nh, left:left + nw] = resized

            # Prepare input tensor
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = image.transpose(2, 0, 1)[None].astype(np.float32) / 255.0

            inp = httpclient.InferInput("images", image.shape, "FP32")
            inp.set_data_from_numpy(image)
            out = httpclient.InferRequestedOutput("output0")

            # Run inference using Triton TensorRT
            result = client.infer("yolo_trt", [inp], outputs=[out])
            pred = result.as_numpy("output0")[0].T

            # Keep car detections only (COCO class ID 2)
            boxes, scores = [], []

            for row in pred:
                class_scores = row[4:]

                if int(np.argmax(class_scores)) != 2:
                    continue

                score = float(np.max(class_scores))
                if score < 0.40:
                    continue

                cx, cy, bw, bh = row[:4]

                x1 = (cx - bw / 2 - left) / scale
                y1 = (cy - bh / 2 - top) / scale
                x2 = (cx + bw / 2 - left) / scale
                y2 = (cy + bh / 2 - top) / scale

                x1, x2 = np.clip([x1, x2], 0, w - 1)
                y1, y2 = np.clip([y1, y2], 0, h - 1)

                if x2 > x1 and y2 > y1:
                    boxes.append([
                        int(x1), int(y1),
                        int(x2 - x1), int(y2 - y1)
                    ])
                    scores.append(score)

            # Remove overlapping duplicate boxes
            keep = (
                cv2.dnn.NMSBoxes(boxes, scores, 0.40, 0.45)
                if boxes else []
            )

            # Keep each detection's original confidence
            detections = []

            for i in np.array(keep).flatten():
                x, y, bw, bh = boxes[i]
                detections.append([
                    x, y, x + bw, y + bh, scores[i], 2
                ])

            data = np.array(detections, dtype=np.float32).reshape(-1, 6)
            tracked_boxes = Boxes(data, orig_shape=(h, w))
            tracks = tracker.update(tracked_boxes, frame)

            # Draw cars and send records to database worker
            for track in tracks:
                x1, y1, x2, y2 = map(int, track[:4])
                car_id = int(track[4])

                # Find the original detection with the highest IoU
                # (overlap) with this tracked box
                confidence = None
                best_iou = 0.0

                for det in detections:
                    dx1, dy1, dx2, dy2, score, class_id = det

                    ix1 = max(x1, int(dx1))
                    iy1 = max(y1, int(dy1))
                    ix2 = min(x2, int(dx2))
                    iy2 = min(y2, int(dy2))

                    intersection = (
                        max(0, ix2 - ix1) * max(0, iy2 - iy1)
                    )

                    track_area = (
                        max(0, x2 - x1) * max(0, y2 - y1)
                    )
                    det_area = (
                        max(0, int(dx2) - int(dx1))
                        * max(0, int(dy2) - int(dy1))
                    )

                    union = track_area + det_area - intersection
                    iou = intersection / union if union > 0 else 0.0

                    if iou > best_iou:
                        best_iou = iou
                        confidence = float(score)

                record = {
                    "car_id": car_id,
                    "vehicle": "car",
                    "model": "yolo_trt",
                    "confidence": confidence,
                    "bbox": [x1, y1, x2, y2],
                    "timestamp": datetime.now(timezone.utc)
                }

                # IPC: send record to the database process
                detection_queue.put(record)
                saved_count += 1

                cv2.rectangle(
                    frame, (x1, y1), (x2, y2), (0, 255, 0), 2
                )
                cv2.putText(
                    frame,
                    f"Car ID: {car_id}",
                    (x1, max(20, y1 - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 255, 0),
                    2
                )

            cv2.imshow("Triton TensorRT Car Tracking", frame)

            # Match original video speed where possible
            elapsed = time.perf_counter() - start
            remaining = max(1, int((frame_time - elapsed) * 1000))

            if cv2.waitKey(remaining) & 0xFF == ord("q"):
                break

    finally:
        if cap is not None:
            cap.release()

        cv2.destroyAllWindows()

        # Finish saving queued records before stopping the worker
        detection_queue.put(None)
        db_process.join()
        detection_queue.close()
        client.close()

        print("Records sent to database worker:", saved_count)


if __name__ == "__main__":
    main()
