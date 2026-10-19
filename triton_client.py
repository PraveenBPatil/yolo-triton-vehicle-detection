
import cv2
import numpy as np
import tritonclient.http as httpclient

# Connect to Triton
client = httpclient.InferenceServerClient("localhost:8000")

# Open video
cap = cv2.VideoCapture("videoplayback.mp4")

if not cap.isOpened():
    raise FileNotFoundError("Cannot open videoplayback.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Keep original frame size
    original_h, original_w = frame.shape[:2]

    # Resize while keeping image proportions
    scale = min(640 / original_w, 640 / original_h)
    new_w = int(original_w * scale)
    new_h = int(original_h * scale)

    resized = cv2.resize(frame, (new_w, new_h))

    # Add padding to make image 640 x 640
    image = np.full((640, 640, 3), 114, dtype=np.uint8)
    left = (640 - new_w) // 2
    top = (640 - new_h) // 2
    image[top:top + new_h, left:left + new_w] = resized

    # Prepare image for Triton
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.transpose(2, 0, 1)[None, ...].astype(np.float32)

    # Send frame to Triton
    inp = httpclient.InferInput("images", image.shape, "FP32")
    inp.set_data_from_numpy(image)
    out = httpclient.InferRequestedOutput("output0")

    result = client.infer(
        model_name="yolo_onnx",
        inputs=[inp],
        outputs=[out]
    )

    # Read model output
    predictions = result.as_numpy("output0")[0].T

    boxes = []
    scores = []

    for row in predictions:
        # The first 4 values are box coordinates
        # The remaining 80 values are class scores
        class_scores = row[4:]
        class_id = int(np.argmax(class_scores))
        confidence = float(class_scores[class_id])

        # Detect cars only
        if class_id == 2 and confidence >= 0.40:
            cx, cy, w, h = row[:4]

            # Remove padding and scale coordinates to original frame
            x1 = int(((cx - w / 2) - left) / scale)
            y1 = int(((cy - h / 2) - top) / scale)
            x2 = int(((cx + w / 2) - left) / scale)
            y2 = int(((cy + h / 2) - top) / scale)

            # Keep coordinates inside the frame
            x1 = max(0, min(x1, original_w - 1))
            y1 = max(0, min(y1, original_h - 1))
            x2 = max(0, min(x2, original_w - 1))
            y2 = max(0, min(y2, original_h - 1))

            if x2 > x1 and y2 > y1:
                boxes.append([x1, y1, x2 - x1, y2 - y1])
                scores.append(confidence)

    # Remove duplicate overlapping boxes
    indexes = cv2.dnn.NMSBoxes(
        boxes, scores, 0.40, 0.45
    )

    # Draw detected cars
    if len(indexes) > 0:
        for i in np.array(indexes).flatten():
            x, y, w, h = boxes[i]

            cv2.rectangle(
                frame, (x, y), (x + w, y + h),
                (0, 255, 0), 2
            )

            cv2.putText(
                frame, f"car: {scores[i]:.2f}",
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (0, 255, 0), 2
            )

    cv2.imshow("Traffic - Cars detected by Triton", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
