# YOLO Vehicle Detection with NVIDIA Triton, TensorRT, and MongoDB

A Python-based vehicle detection project that uses YOLO, NVIDIA Triton Inference Server, TensorRT, multiprocessing, and MongoDB to detect vehicles in video and store detection results.

## Project Overview

This project demonstrates an object detection pipeline in which video frames are processed by a YOLO model served through NVIDIA Triton Inference Server. Detection results are passed between processes using Python multiprocessing and saved in MongoDB.

## Vehicle Detection Demo

![Vehicle Detection Demo](vehicle-detection-demo.png)

## Technologies Used

- **Python** — application logic and video processing
- **YOLO** — vehicle detection
- **OpenCV** — video reading and image preprocessing
- **NVIDIA Triton Inference Server** — model serving
- **TensorRT** — optimized inference engine
- **ONNX** — model interchange format
- **Python multiprocessing** — communication between processes using queues
- **MongoDB** — storage of vehicle detection records

## Architecture

```text
Input Video
    |
    v
OpenCV Frame Processing
    |
    v
YOLO Model on Triton Inference Server
    |
    v
Vehicle Detection and Tracking
    |
    v
Multiprocessing Queue
    |
    v
MongoDB Worker Process
    |
    v
Stored Detection Records
```

## Main Features

- Vehicle detection in video frames
- YOLO model inference through Triton
- ONNX model deployment
- TensorRT inference configuration
- Python multiprocessing and inter-process communication (IPC)
- MongoDB storage of detection results
- Basic examples for MongoDB CRUD operations and multiprocessing

## Project Structure

```text
yolo-triton-vehicle-detection/
├── model_repository/
│   ├── yolo_onnx/
│   │   ├── 1/
│   │   │   └── model.onnx
│   │   └── config.pbtxt
│   └── yolo_trt/
│       └── config.pbtxt
├── detection_ipc_mongodb.py
├── triton_client.py
├── triton_video.py
├── multiprocessing_demo.py
├── ipc_demo.py
├── ipc_pipe.py
├── ipc_two_way.py
├── ipc_shared_memory.py
├── ipc_workers.py
├── ipc_task_processor.py
├── ipc_error_handling.py
├── threading_demo.py
├── mongodb_demo.py
├── mongodb_read.py
├── mongodb_read_all.py
├── mongodb_insert_many.py
├── mongodb_filter.py
├── mongodb_update.py
├── mongodb_delete.py
├── mongodb_detection_test.py
├── yolo26n.onnx
└── .gitignore
```

## Requirements

- Python
- Docker Desktop with a working Linux container engine
- NVIDIA GPU and compatible NVIDIA container runtime for GPU-based TensorRT inference
- NVIDIA Triton Inference Server
- MongoDB
- Python packages required by the application scripts

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/PraveenBPatil/yolo-triton-vehicle-detection.git
cd yolo-triton-vehicle-detection
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the Python packages required by the scripts. Check the imports in each script to identify the required packages.

### 3. Start MongoDB

Run MongoDB locally or through Docker. Ensure the connection URI used by the application matches your MongoDB setup.

### 4. Start Triton Inference Server

Configure the model repository and start Triton with the required model files and GPU support. See the NVIDIA Triton documentation for the appropriate Docker command.

### 5. Run the application

Run the relevant Python script from the project directory after configuring the video path, Triton endpoint, and MongoDB connection.

## Learning Objectives

This project provides practical experience with:

- Object detection using YOLO
- Model serving with Triton Inference Server
- ONNX and TensorRT deployment concepts
- Python multiprocessing and IPC
- MongoDB document storage and queries
- Integrating computer vision with a database pipeline

## Future Improvements

- Add automated tests
- Add configurable application settings
- Improve logging and error handling
- Document model deployment commands
- Add sample output screenshots

## Author

**Praveen B. Patil**

GitHub: [PraveenBPatil](https://github.com/PraveenBPatil)
