import argparse
import Files.OCR as OCR 
import Files.image_inference as image_inference
from Files.screen_coords import *
import Files.champs_list as file
import time
import sys
from pynput.keyboard import Listener, KeyCode, Controller, Key
import threading

overlay_app = None

def set_overlay_app(app):
    global overlay_app
    overlay_app = app

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-skp', '--simulate-keys', action='store_true', 
                        help='Enable simulation of key presses')
    args = parser.parse_args()

    if args.simulate_keys:
        print("Simulating keyboard input...\n\n\n")

    listener_thread = threading.Thread(target=start_listener, daemon=True)
    listener_thread.start()
    listener_thread.join()  

def start_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()

def shopToOCR():
    try:
        screenshot = OCR.capture(())
        return processOCR(screenshot)
    except Exception as e:
        print(f"Error in shopToOCR: {e}", file=sys.stderr)
        # Log the error details here

def processOCR(screenshot):
    text_list = [] 
    try:
        for i in range(5):
            bbox = (
                CHAMP_TEXT_LEFT + (i * CHAMP_SPACING), 
                CHAMP_TEXT_TOP, CHAMP_TEXT_RIGHT + 
                (i * CHAMP_SPACING), CHAMP_TEXT_BOTTOM
                )
            target_string = OCR.ocr(bbox, screenshot)
            closest = file.find_closest(target_string, file.set10_champs)
            text_list.append(closest)
        update2(text_list)
        print("shopToOCR Done!")  

    except Exception as e:
        print(f"Error in processOCR: {e}")

def boardToModel():
    keyboard = Controller() 
    SimulatePressedKeys = False

    try:
        print("Capturing screenshots for board modeling...")
        screenshots = []
        for index in range(8):
            if SimulatePressedKeys: 
                keyboard.press('q')
                keyboard.release('q')
            time.sleep(1)
            screenshot = OCR.capture(())
            screenshots.append(screenshot)
            print(f"Captured screenshot #{index + 1}")

        print("Processing screenshots...")
        champions = image_inference.process_screenshots(screenshots)
        if not champions:
            print("No champions processed or an error occurred.")
            return
        
        ''' RETURN CONTENT '''
        tally = {champion: champions.count(champion) for champion in set(champions)}
        champPool = file.champPool
        champion_info = file.champion_info
        stats_output = getStats(tally, champion_info, champPool)
        updateOverlay(stats_output)
        print("boardToModel Done!")  

    except Exception as e:
        print(f"Error in boardToModel: {e}")

def on_press(key):
    try:
        ''' HERE IS WHERE THE KEYBINDS ARE HANDLED. '''
        # OCR
        if key == KeyCode.from_char('d'):
            print("d key pressed! \n ShopToOCR Running...")
            shopToOCR()
            '''
            List of things shopToOCR() does
            1. Captures screenshot
            2. Processes screenshot
            3. Runs OCR on the 5 champion areas
            4. Outlines desired champions in red
            '''

        # BOARDTOMODEL
        elif key == KeyCode.from_char('\\'):
            print("] key pressed! \n boardToModel Running...")
            boardToModel()
            '''
            List of things boardToModel() does
            1. Captures screenshots
            2. Processes screenshots
            3. Runs inference on the screenshots
            4. Create a list of champion names and their counts
            4. Updates the overlay
            '''

        # DEBUG KEYBIND
        elif key == KeyCode.from_char('='):
            print("'=' key pressed! Triggering update_overlay for debugging.")
            debug = {
            1: [("ChampionA1", 5), ("ChampionB1", 3), ("ChampionC1", 2)],
            2: [("ChampionA2", 4), ("ChampionB2", 3)],
            3: [("ChampionA3", 6), ("ChampionB3", 4), ("ChampionC3", 1)],
            4: [("ChampionA4", 2), ("ChampionB4", 1)]
            }
            updateOverlay(debug)

        # UPDATE DEBUG KEYBIND
        elif key == KeyCode.from_char('-'):
            print("'-' key pressed! CHANGING CONTENTS.")
            debug = {
                1: [("ChampionTest1", 4), ("ChampionTest2", 3)],
                2: [("ChampionTest3", 5), ("ChampionTest4", 2)],
                3: [("ChampionTest5", 6), ("ChampionTest6", 1)]
            }
            updateOverlay(debug)

        # QUIT APPLICATIONS
        elif key == KeyCode.from_char('['):
            print("Exiting program.")
            sys.exit(0)

    except Exception as e:
        print(f"Error in on_press: {e}")


''' HERE IS WHERE THE STATS FROM boardToModel() ARE HANDLED. '''
def getStats(tally, champion_info, champPool):
    champions_by_cost = {}
    for name, count in tally.items():
        if name in champion_info and count > 0:
            champ_cost = champion_info[name]["cost"]
            if champ_cost not in champions_by_cost:
                champions_by_cost[champ_cost] = []
            champions_by_cost[champ_cost].append((name, count))

    top_champions = {}
    for cost, champs in champions_by_cost.items():
        sorted_champs = sorted(champs, key=lambda x: x[1], reverse=True)[:3]
        top_champions[cost] = sorted_champs

    return top_champions

''' Sends signal containing the dictionary to update the overlay textbox. '''
def updateOverlay(stats_output):
    global overlay_app  # Ensure this is the instance of your overlay app
    overlay_app.custom_window.update_signal.emit(stats_output)

def update2(curr_shop):
    global overlay_app  # Ensure this is the instance of your overlay app
    overlay_app.custom_window.update2.emit(curr_shop)
