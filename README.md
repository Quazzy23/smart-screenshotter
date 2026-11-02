# 📸 Smart-Screenshotter

**Smart-Screenshotter** is a lightweight Windows utility that replaces the default `Print Screen` behavior. It silently intercepts the key press, takes a full-screen screenshot, and saves it with a sortable timestamp (`YYYY-MM-DD_HH-MM-SS.png`). No Snipping Tool pop-ups, no OneDrive syncing, no UI clutter.

---

## 🌟 Key Features

*   **100% Local & Private:** No cloud syncing or accounts.
*   **Silent Background Operation:** Runs invisibly via Windows Task Scheduler (no tray icon).
*   **Custom Save Location:** Define exactly where screenshots are stored.
*   **Clean Filenames:** Auto-names files with exact date and time.
*   **Easy Management:** Simple batch files for install, path change, and uninstall.

---

## 🚀 Installation & Setup

### 1. Get the Project
Download the latest `.zip` from [Releases](https://github.com/Quazzy23/Smart-Screenshotter/releases), or clone the repo.

### 2. Install & Configure
Run **`install_service.bat`** as Administrator. 
* Enter your desired save path (e.g., `D:\Pictures\Screenshots`).
* The task is registered and started automatically.
* Verify execution via `taskschd.msc` (ensure `SmartScreenshotterService` state is **Running**).
* *To pause the service, select "End" or "Disable".*

### 3. Usage
Press **`Print Screen`**. The screenshot is instantly saved to your folder.

### 4. Change Save Path
Run **`install_service.bat`** again as Administrator. The script stops the old task, asks for a new path, and restarts the service.

### 5. Uninstallation
Run **`uninstall_service.bat`** as Administrator to remove the task.

---

## 👥 Authors
*   **Project Lead:** Quazzy ([@Quazzy23](https://github.com/Quazzy23))
*   **Development:** Created with the support of DeepSeek.