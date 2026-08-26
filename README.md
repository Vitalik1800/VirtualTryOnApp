# Virtual Try-On App

A desktop application for virtually trying on accessories using computer vision and facial landmark detection.

The application allows users to select an accessory and see it rendered on their face in real time using a camera.

## Features

* Real-time virtual accessory try-on
* Face landmark detection
* Support for multiple accessory categories
* Glasses, hats, and masks
* Accessory management through a SQLite database
* REST API built with FastAPI
* Desktop GUI
* Camera-based image processing
* Packaged Windows executable using PyInstaller

## Supported Accessories

The application currently provides three accessory categories:

* **Glasses** - 20 accessories
* **Hats** - 20 accessories
* **Masks** - 20 accessories

The application also contains additional test accessories used during development and integration testing.

## Technologies

### Programming Language

* Python 3.12

### Computer Vision

* OpenCV
* MediaPipe

### Backend

* FastAPI
* Uvicorn
* SQLAlchemy
* SQLite

### Desktop Application

* CustomTkinter
* Tkinter

### HTTP Communication

* Requests

### Packaging

* PyInstaller

## Project Structure

```text
VirtualTryOnApp/
│
├── assets/
│   └── accessories/
│       ├── glasses/
│       ├── hats/
│       └── masks/
│
├── client/
│   ├── api/
│   ├── gui/
│   ├── services/
│   └── ...
│
├── server/
│   ├── api/
│   ├── database/
│   ├── models/
│   └── main.py
│
├── tests/
│
├── virtual_try_on.db
├── requirements.txt
├── README.md
└── run.py
```

## Architecture

The application is divided into several main components:

```text
Desktop Client
      │
      │ HTTP
      ▼
FastAPI Server
      │
      ├── Accessory API
      │
      └── Try-On API
      │
      ▼
SQLite Database
```

The desktop client communicates with the FastAPI server through HTTP requests.

The server provides accessory data stored in the SQLite database. The client uses this data to display the available accessories and perform virtual try-on operations.

## Database

The application uses SQLite as its database.

The database file is:

```text
virtual_try_on.db
```

The `accessories` table stores information about available accessories.

Each accessory contains:

* `id`
* `name`
* `category`
* `file_path`
* `is_active`

Only active accessories are returned by the accessory API.

## API

The FastAPI server runs locally on:

```text
http://127.0.0.1:8000
```

### Root Endpoint

```http
GET /
```

Response:

```json
{
    "message": "Virtual Try-On API is running"
}
```

### Accessories Endpoint

```http
GET /accessories/
```

Returns a list of active accessories.

Example:

```json
[
    {
        "id": 1,
        "name": "glasses_01",
        "category": "Glasses",
        "file_path": "assets\\accessories\\glasses\\glasses_01.png"
    }
]
```

## Installation

### 1. Clone or copy the project

Place the project in a local directory.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application from Source

Start the FastAPI server:

```bash
uvicorn server.main:app --host 127.0.0.1 --port 8000
```

The server should display:

```text
Uvicorn running on http://127.0.0.1:8000
```

Then start the desktop application:

```bash
python run.py
```

## Running the Windows Executable

A packaged Windows version is available in:

```text
dist/VirtualTryOnApp/
```

Run:

```text
dist/VirtualTryOnApp/VirtualTryOnApp.exe
```

The application should be launched from the `dist` directory.

The `build` directory is an intermediate PyInstaller build directory and is not intended for normal application execution.

## API Connection

The desktop client uses the following API address:

```text
http://127.0.0.1:8000
```

The accessory API client requests:

```http
GET http://127.0.0.1:8000/accessories/
```

A running FastAPI server is therefore required when using the current client-server configuration.

## Testing

The project includes tests for different application components, including:

* API functionality
* SQLite database integration
* Accessory loading
* System integration
* Virtual try-on functionality

Test accessories may be present in the database as a result of integration and system testing.

## Building the Executable

The application can be packaged with PyInstaller.

After building, the main executable is located at:

```text
dist/VirtualTryOnApp/VirtualTryOnApp.exe
```

The complete `dist/VirtualTryOnApp` directory should be preserved because the application uses the PyInstaller onedir distribution.

Do not copy only the `.exe` file.

## Requirements

* Windows 10 or later
* Python 3.12 for running from source
* Webcam for real-time try-on
* Sufficient system resources for OpenCV and MediaPipe

## Troubleshooting

### The application does not start by double-clicking the EXE

Make sure the complete directory is present:

```text
dist/
└── VirtualTryOnApp/
    ├── VirtualTryOnApp.exe
    └── _internal/
        └── ...
```

The executable should be launched from the `dist/VirtualTryOnApp` directory.

The `build/VirtualTryOnApp` directory is not the final distribution directory.

### Accessories cannot be loaded

Make sure the FastAPI server is running:

```bash
uvicorn server.main:app --host 127.0.0.1 --port 8000
```

Then verify the API:

```bash
curl http://127.0.0.1:8000/
```

Expected response:

```json
{
    "message": "Virtual Try-On API is running"
}
```

You can also verify the accessories endpoint:

```bash
curl http://127.0.0.1:8000/accessories/
```

## Project Status

The project includes:

* Desktop application
* FastAPI backend
* SQLite database
* Accessory database
* Computer vision processing
* Virtual accessory rendering
* Automated tests
* Windows executable build
* Project documentation

The application is prepared as a functional desktop prototype for virtual accessory try-on.

## License

This project was developed as part of a diploma project.

Unless otherwise stated, the source code and project assets are intended for educational and demonstration purposes.
