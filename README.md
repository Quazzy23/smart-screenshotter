# 📸 Smart-Screenshotter

**Smart-Screenshotter** is a lightweight Windows utility that completely replaces the default `Print Screen` behavior. It silently intercepts the key press and provides two capture modes: a fast full-screen screenshot with a smooth fade animation, or a custom area selection with a familiar snip-overlay interface.

---

## 🌟 Key Features

*   **100% Local & Private:** No cloud syncing, no accounts.
*   **Dual Capture Modes:** Full-screen and area selection.
*   **Silent Background Operation:** Runs invisibly via Windows Task Scheduler (no tray icon).
*   **Custom Save Location:** Define exactly where screenshots are stored.
*   **Clean Filenames:** Auto-names files with exact date and time.

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
* Press **`Print Screen`** for a full-screen capture (with a smooth fade animation).
* Press **`Alt + Print Screen`** to open the snipping overlay and select a specific area.

### 4. Change Save Path or Uninstall
*   **Change Path:** Run `install_service.bat` again as Administrator to update the path.
*   **Uninstall:** Run `uninstall_service.bat` as Administrator to remove the task.

---

## 👥 Authors
*   **Project Lead:** Quazzy ([@Quazzy23](https://github.com/Quazzy23))
*   **Development:** Created with the support of DeepSeek.