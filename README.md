# WebP Sequence Converter

A Python-based desktop application with a graphical user interface (GUI) that converts sequences of images (PNG, JPG, TIFF, etc.) into animated WebP files.

## Features
- **Auto-Sequence Detection**: Automatically groups images in a directory by their filename prefixes into sequences (e.g., `walk_001.png`, `walk_002.png`).
- **Customizable FPS & Quality**: Adjust the frames per second (FPS) and output WebP compression quality (1-100).
- **Resizing**: Check the option to resize the animated WebP to a specific width and height (uses high-quality LANCZOS resampling).
- **Standalone App**: Wrapped into a `.app` bundle for macOS and a `.exe` for Windows.

## Installation & Usage

### 🍎 For Mac Users (macOS)
The Mac version runs via a provided shortcut script that sets up the environment automatically.

1. Clone or download this repository to your Mac.
2. Open the `webp_app` folder in Finder.
3. Double-click **`start_app.command`**.
   *(Note: The first time you run it, your Mac might say it's from an "unidentified developer". If so, right-click `start_app.command` and select **Open**).*
4. The script will automatically install necessary dependencies (like `customtkinter` and `Pillow`) and launch the application!

*Alternatively, you can run it manually via terminal:*
```bash
pip install -r requirements.txt
python main.py
```

### 🪟 For Windows Users (Windows 11)
The Windows version is compiled into a single, standalone executable `.exe` file. **You do not need to install Python to run it.**

1. Go to the **[Releases page](../../releases/latest)** of this repository on GitHub.
2. Under the **Assets** section of the latest release, click on **`WebP-Converter-Windows.exe`** to download it.
3. Once downloaded, simply double-click **`WebP-Converter-Windows.exe`** to launch the app!
   *(Note: Windows SmartScreen may show a "Windows protected your PC" warning since this is a self-published app. Click **More info** -> **Run anyway**).*

## How to Convert Images

1. **Input Directory**: Click "Browse" and select a folder containing your image sequence(s).
2. **Select Sequence**: Choose the detected image sequence from the dropdown menu. It will display the number of frames found.
3. **Output File**: Choose where to save the resulting `.webp` animation.
4. **Adjust Settings**: Set the desired FPS and Quality.
5. **Resize (Optional)**: Check "Resize Output?" to input a specific width and height for your final WebP file.
6. **Convert**: Click **Convert to WebP** and wait for the success message.
