"""
Title: pressingKeys
Description: This is a program to press keys given some text.
Author: Marco A. Barreto - marcoagbarreto
Version: 13-Aug-2022
"""

try:
    from os import system as os_system, name as os_name
    from time import sleep as time_sleep, time as time_time
    from keyboard import press as keyboard_press, release as keyboard_release, is_pressed as keyboard_is_pressed, wait as keyboard_wait
    from random import uniform as random_uniform
    from re import sub as re_sub, findall as re_findall
    from pyperclip import paste as pyperclip_paste
except ImportError as details:
    print("-E- Couldn't import module, try pip install 'module'")
    raise details


def key_press(key):
    # sleeps to avoid key ghosting from previous key press
    time_sleep(random_uniform(0.07, 0.09))
    keyboard_press(key)
    # sleeps between 0.05 and 0.07 seconds to simulate natural pressing
    time_sleep(random_uniform(0.05, 0.07))
    keyboard_release(key)


class PressingKeys:
    def __init__(self, file):

        self.keyList = file
        self.parse_text()

    def parse_text(self):
        self.keyList = self.keyList.replace('\n', '')
        self.keyList = self.keyList.replace('.', '')
        self.keyList = re_sub(r'[0-9]', '', self.keyList)
        self.keyList = re_findall('left|right|up|down|', self.keyList)
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

        start_key = 'Ctrl'
        abort_key = 'Q'
        print("Press ", [start_key], " to start.")
        keyboard_wait(start_key)
        print("Started, press", [abort_key], "to abort.")

        t0 = time_time()
        # Starts pressing keys
        for key in self.keyList:
            if key:
                key_press(key)
            if keyboard_is_pressed(abort_key):
                print('Aborted')
                break

        t1 = time_time()
        print('Finished')
        print('Time delayed:', int(t1 - t0), 's')


def main():
    copy_key = 'Ctrl+C'
    restart_key = 'Shift'

    # Set terminal size to optimal size
    os_system('mode con cols=37 lines=12')

    # Set terminal to be always on top
    os_system('Powershell.exe -ExecutionPolicy UnRestricted -Command "(Add-Type -memberDefinition \\"[DllImport('
              '\\"\\"user32.dll\\"\\")] public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter, '
              'int x,int y,int cx, int xy, uint flagsw);\\" -name \\"Win32SetWindowPos\\" -passThru )::SetWindowPos(('
              'Add-Type -memberDefinition \\"[DllImport(\\"\\"Kernel32.dll\\"\\")] public static extern IntPtr '
              'GetConsoleWindow();\\" -name \\"Win32GetConsoleWindow\\" -passThru )::GetConsoleWindow(),-1,0,0,0,0,'
              '67)"')

    # Clear the terminal after last command
    os_system('cls' if os_name == 'nt' else 'clear')

    while True:
        # Copy the key list
        print('Waiting for items in the clipboard,\nuse',
              [copy_key], 'to copy the key list.')
        keyboard_wait(copy_key)
        time_sleep(0.1)  # Sleep 0.1 s so clipboard can refresh

        # Run the program
        PressingKeys(pyperclip_paste()).run()

        # Restart the program
        print('Press', [restart_key], 'to start again.')
        keyboard_wait(restart_key)
        os_system('cls' if os_name == 'nt' else 'clear')


if __name__ == '__main__':
    main()
