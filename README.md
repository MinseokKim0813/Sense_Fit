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
- **pandas / numpy** (for data analysis)

---

## Features

✅ Create multiple user profiles (Name + DPI)  
✅ Real-time global mouse cursor tracking  
✅ Automatic session logging (timestamp, X, Y, click status)  
✅ Intelligent data validation:
- Minimum data length
- Consistent timestamps
- Reasonable screen positions
- No unrealistic cursor jumps or endless jittering  
✅ Post-tracking analysis:
- Find where users **paused** during movement
- Detect **overshoot corrections** when moving toward targets
✅ Clear separation between **Frontend** (UI) and **Backend** (tracking, analysis logic)

---

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

---

## Installation

### 1. Set up a virtual environment

#### On Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### On macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` appear in your terminal prompt.

---

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

*Typical libraries include*:
- PyQt5
- pyautogui
- pandas
- numpy

---

## Running the Application

```bash
python main.py
```

This will launch the **Profile Selection Page**.  
From there, you can create new profiles and start tracking sessions.

---

## Project Structure

```plaintext
Sense_Fit/
├── Frontend/
│   ├── frontmain.py        # Main interface (profile selection, navigation)
│   ├── create_profile.py   # Popup to create new profile
│   ├── profile_main.py     # Profile-specific tracking window
│   ├── error_window.py     # Popup for any errors detected
│
├── Backend/
│   ├── tracking_module.py  # Handles live cursor tracking
│   ├── analyze_module.py   # Post-tracking data analysis
│   ├── create_profile.py   # Profile data management (JSON storage)
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

- **Create a Profile** → Select a profile → **Start tracking**.
- The system records **(timestamp, x, y, click status)** every few milliseconds.
- After stopping tracking, the system:
  - Validates collected data.
  - Identifies **pauses** where the mouse stayed still.
  - Detects **overshoot behaviors** where the cursor reversed direction sharply.
  - Prepares the session log for further analysis or visualization.

---

## Future Improvements

- Visualize tracking path on a graph (pause points, overshoots, etc.)
- Export analysis results into a report.
- Add basic recommendations based on user movement patterns.
- More robust error handling and UI polish.

---

## Authors

- Primary Developer: **Kyrie Park**, **Yongje Jeon**, **Junyong Moon**, **Minseok Kim**
- Special thanks to the iterative brainstorming and prototyping sessions!

---

# ✨ Let's keep building!

---

---
