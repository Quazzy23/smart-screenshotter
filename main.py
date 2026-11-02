import keyboard
import time
from PIL import ImageGrab
import os
import json
import sys
from datetime import datetime

def get_save_path():
    config_file = "config.json"
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    config_path = os.path.join(base_dir, config_file)
    
    if not os.path.exists(config_path):
        print(f"Error: '{config_file}' not found! Run install.bat")
        return None
        
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            # Берем путь и на всякий случай чиним слеши
            path = config.get("save_directory", "").replace('\\\\', '\\')
            if not path:
                print("Error: Save path not specified! Run install.bat")
                return None
            return path
    except Exception as e:
        print(f"Error reading config: {e}")
        return None

def take_screenshot(save_dir):
    time.sleep(0.1) 
    try:
        screenshot = ImageGrab.grab()
        now = datetime.now()
        filename = now.strftime("%Y-%m-%d_%H-%M-%S") + ".png"
        filepath = os.path.join(save_dir, filename)
        screenshot.save(filepath)
        print(f"Screenshot saved: {filename}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    save_dir = get_save_path()
    if not save_dir:
        time.sleep(5)
        sys.exit(1)
        
    if not os.path.exists(save_dir):
        try:
            os.makedirs(save_dir)
        except Exception as e:
            print(f"Failed to create directory: {e}")
            sys.exit(1)

    print(f"Saving to: {save_dir}")
    print("Press Print Screen to take a screenshot.")
    
    keyboard.add_hotkey('print screen', lambda: take_screenshot(save_dir), suppress=True)
    keyboard.wait()