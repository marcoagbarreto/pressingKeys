"""
Title: pressingKeys
Description: This is a program to press keys given some text.
Author: Marco A. Barreto - marcoagbarreto
Version: 13-Aug-2022
"""

try:
    import os
    import time
    import keyboard
    import numpy as np
    import re
    import pyperclip
except ImportError as details:
    print("-E- Couldn't import module, try pip install 'module'")
    raise details


def key_press(key):
    # sleeps to avoid key ghosting from previous key press
    time.sleep(np.random.uniform(0.07, 0.09))
    keyboard.press(key)
    # sleeps between 0.05 and 0.07 seconds to simulate natural pressing
    time.sleep(np.random.uniform(0.05, 0.07))
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
        # Map keys to match inverted logic
        for index, key in enumerate(self.keyList):
            if key == 'left':
                self.keyList[index] = 'right'

            elif key == 'right':
                self.keyList[index] = 'left'

            elif key == 'up':
                self.keyList[index] = 'down'

            elif key == 'down':
                self.keyList[index] = 'up'

        # Remove empty items in the list
        for index, key in enumerate(self.keyList):
            if key == '':
                del self.keyList[index]

    def run(self):
        print('Ensure to have focus on the app.')
        # Show the amount of keys to press
        print('Keys to press: ', len(self.keyList))

        startkey = 'Ctrl'
        abortkey = 'Q'
        print("Press ", [startkey], " to start.")
        keyboard.wait(startkey)
        print("Started, press", [abortkey], "to abort.")

        t0 = time.time()
        # Starts pressing keys
        for key in self.keyList:
            if key:
                key_press(key)
            if keyboard.is_pressed(abortkey):
                print('Aborted')
                break

        t1 = time.time()
        print('Finished')
        print('Time delayed:', int(t1 - t0), 's')


def main():
    copykey = 'Ctrl+C'
    restartkey = 'Shift'

    # Set terminal size to optimal size
    os.system('mode con cols=37 lines=12')

    # Set terminal to be always on top
    os.system('Powershell.exe -ExecutionPolicy UnRestricted -Command "(Add-Type -memberDefinition \\"[DllImport('
              '\\"\\"user32.dll\\"\\")] public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter, '
              'int x,int y,int cx, int xy, uint flagsw);\\" -name \\"Win32SetWindowPos\\" -passThru )::SetWindowPos(('
              'Add-Type -memberDefinition \\"[DllImport(\\"\\"Kernel32.dll\\"\\")] public static extern IntPtr '
              'GetConsoleWindow();\\" -name \\"Win32GetConsoleWindow\\" -passThru )::GetConsoleWindow(),-1,0,0,0,0,'
              '67)"')

    # Clear the terminal after last command
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        # Copy the key list
        print('Waiting for items in the clipboard,\nuse',
              [copykey], 'to copy the key list.')
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
