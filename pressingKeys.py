"""
Title:
Description: This is a program to press keys given a text file
Author: Marco A. Barreto - marcoagbarreto
Version: 29-07-2022
"""

try:
    import os
    import time
    import keyboard
    import random
    import numpy as np
    import re
    import pyperclip
except ImportError as details:
    print("-E- Couldn't import module, try pip install 'module'")
    raise details


def key_press(key):
    time.sleep(0.07)  # sleeps to avoid key ghosting from previous key press
    keyboard.press(key)
    time.sleep(np.random.uniform(0.05, 0.07))  # sleeps between 0.05 and 0.07 seconds to simulate natural pressing
    keyboard.release(key)


class PressingKeys:
    def __init__(self, file):

        self.keyList = file
        self.parse_text()

    def parse_text(self):
        self.keyList = self.keyList.replace('\n', '')
        self.keyList = self.keyList.replace('.', '')
        self.keyList = re.sub(r'[0-9]', '', self.keyList)
        self.keyList = re.findall('left|right|up|down|', self.keyList)
        return self.key_maps()

    def key_maps(self):
        for i in range(len(self.keyList)):
            if self.keyList[i] == 'left':
                self.keyList[i] = 'right'

            elif self.keyList[i] == 'right':
                self.keyList[i] = 'left'

            elif self.keyList[i] == 'up':
                self.keyList[i] = 'down'

            elif self.keyList[i] == 'down':
                self.keyList[i] = 'up'

    def run(self):
        print('Ensure to have focus on the app.')
        # Show the amount of keys to press
        print('Keys to press: ', len(self.keyList))

        starter = 'ctrl'
        print("Press ", [starter], " to start.")
        keyboard.wait(starter)
        print("Started, press", ["Q"], "to abort.")

        t0 = time.time()
        # Starts pressing keys
        for key in self.keyList:
            if key:
                key_press(key)
            if keyboard.is_pressed('q'):
                print('Aborted')
                break

        t1 = time.time()
        print('Finished')
        print('Time delayed:', int(t1 - t0), 's')



def main():
    copykey = 'ctrl+c'
    restartkey = 'shift'

    while True:
        # Copy the key list
        print('Waiting for items in the clipboard, use', [copykey], 'to copy the key list')
        keyboard.wait(copykey)
        time.sleep(0.1)  # Sleep 0.1 s so clipboard can refresh

        # Run the program
        PressingKeys(pyperclip.paste()).run()

        # Restart the program
        print('Press', [restartkey], 'to start again.')
        keyboard.wait(restartkey)
        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    main()
