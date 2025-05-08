# Sense Fit

A desktop application built with PyQt5 that **tracks**, **analyzes**, and **visualizes** mouse movement patterns to better understand user behavior.

---

## Overview

Sense Fit is a **multi-featured Python desktop application** that:

- Allows users to **create personalized profiles** with their own DPI settings.
- **Tracks** real-time mouse cursor movements and clicks.
- **Analyzes** cursor movement paths, detecting:
  - **Pause segments** (when the cursor stops moving).
  - **Overshoot behaviors** (when the user moves too far past their intended target).
- Provides an **interactive GUI** to manage profiles, track sessions, and view tracking results.

Built using:

- **PyQt5** (GUI Framework)
- **pyautogui** (for cursor tracking)
- **pyqtgraph** (for data visualization)
- **pytest** (for coverage report)

---

## Features

- Create multiple user profiles (Name + DPI)
- Real-time global mouse cursor tracking
- Automatic session logging (timestamp, X, Y, click status)
- Intelligent data validation:

  - Minimum data length
  - Consistent timestamps
  - Reasonable screen positions
  - No unrealistic cursor jumps or endless jittering

- Post-tracking analysis:

  - Find where users **paused** during movement
  - Detect **overshoot corrections** when moving toward targets

- Clear separation between **Frontend** (UI) and **Backend** (tracking, analysis logic)

---

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

---

## Installation

You will use **terminal** to set up and run the application.

First, move to your desired repository:

```
cd /path/to/dir
```

### 1. Clone this repository

```
git clone https://github.com/MinseokKim0813/Sense_Fit.git
cd Sense_Fit
```

### 2. Set up a virtual environment and install dependencies

#### On Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### On MacOS
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` appear in your terminal prompt.

Then to install python libraries (for both Windows and MacOS):
```
pip install -r requirements.txt
```

_If the script does not run, try `pip3 install -r requirements.txt`._

You may use `deactivate` to exit from the virtual environment.

When you come back later, simply run `.venv\Scripts\activate` or `source .venv/bin/activate` to re-activate the virtual environment.

---

## Running the Application

```bash
make run
```

This will launch the **Profile Selection Page**.  
From there, you can create new profiles and start tracking sessions.

---

## Running Tests

## How to get Coverage Report

```bash
make coverage
```

This command executes all tests located in the `Tests/` directory, including both unit tests and system tests. It generates a comprehensive coverage report that is displayed in the terminal and also saved as an HTML file at `htmlcov/index.html`. You can view the HTML report in any web browser for a more detailed analysis of the test coverage.

---

## Project Structure

```plaintext
Sense_Fit/
├── Frontend/
│   ├── frontmain.py        # Main interface (profile selection, navigation)
│   ├── create_profile.py   # Popup to create new profile
│   ├── profile_main.py     # Profile-specific tracking window
│   └── error_window.py     # Popup for any errors detected
│
├── Backend/
│   ├── tracking_module.py  # Handles live cursor tracking
│   ├── analyze_module.py   # Post-tracking data analysis
│   └── create_profile.py   # Profile data management (JSON storage)
│
├── Tests/
│   ├── System              # Test suite for System Testing (Specialized for frontend)
│   ├── Unit_Testing        # Test suite for Unit Testing (Specialized for backend)
│   └── conftest.py         # Fixtures for Unit Testing
│
├── storage/
│   ├── profiles.json       # Stored user profiles
│   └── logs/               # Session logs (cursor movement data)
│
├── requirements.txt        # Python dependencies
├── main.py                 # Main application
└── README.md               # Project overview (this file)
```

---

## How It Works (Brief)

- **Create a Profile** or Select a profile → **Start tracking**.
- The system records **(timestamp, x, y, click status)** every 10 milliseconds.
- After stopping tracking, the system:
  - Validates collected data.
  - Identifies **Pauses**, **Start Positions**, and **End Positions**.
  - Detects **overshoot** and **staccato** behaviors.
- After the user agrees to get a calculation, the system suggests a suitable DPI than the one user had before.
- The user can later check the **Distance Traveled** and **DPI Suggestion History** graph for insights.

---

## Future Improvements

- Visualize tracking path on a graph (pause points, overshoots, etc.)
- Export analysis results into a report.
- More robust error handling and UI polish.
- Allow profile deletion.

---

## Authors

- Primary Developers: **Kyrie Park**, **Yongje Jeon**, **Junyong Moon**, **Minseok Kim**
- Special thanks to the iterative brainstorming and prototyping sessions!
