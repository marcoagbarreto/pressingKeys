try:
    import os
    import time
    import keyboard
    import random
    import numpy as np
    import re
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

        self.keyList = None
        self.file = file
        self.read_text()

    def read_text(self):
        with open(self.file, 'r') as file:
            self.keyList = file.read()
        return self.parse_text()

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

        # Starts pressing keys
        for key in self.keyList:
            if key:
                key_press(key)
            if keyboard.is_pressed('q'):
                print('Aborted')
                break

        print('Finished')


if __name__ == '__main__':

    file_name = 'keyList.txt'

    try:
        if os.stat(file_name).st_size > 0:
            print("Found ", file_name)
        else:
            print("Empty file", file_name)
    except FileNotFoundError:
        print('Missing, creating file ', file_name)
        f = open(file_name, "a")
        f.close()

    t0 = time.time()
    PressingKeys(file_name).run()
    t1 = time.time()
    print('Time delayed:', int(t1 - t0), 's')
    print('Close the window to exit.')
    keyboard.wait()
