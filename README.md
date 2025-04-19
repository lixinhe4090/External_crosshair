# Crosshair Customizer 🎯

# If you like this project, please consider giving it a star on GitHub! 🌟 Thank you for your support!🙏

### Sorry, due to GitHub's upload limitations, you'll need to package your own binaries to use all the features.😫

# Changelog:
## March 23, 2025 😄：
  --**Fixed**: Due to game reasons, the mouse is centered, and the Windows layer logic is started when firing, resulting in the game screen being overwritten and unable to fire

  --**Added**: Added a new shortcut command: Ctrl+W, you can use this shortcut to quickly close the program (only for Windows)

  **Note**: You can't change the name of the program, because the only condition to close the program is to make the name of the program "External_crosshair.exe"

## In the (very) early morning of April 5, 2025 😴：
  -- **Fixed**:Using a new idea - Pygame dependency library, it effectively solves the problem of layer occupation in Windows

  -- **Added**:You can now use the Page UP/DOWN and Ctrl W key combination at any time to enable global listening

## April 6, 2025 🌟：
  - **Added**: Added new hotkey functionality for `F1` to `F8` to provide more control over the crosshair customization.
    - `F1`, `F2`, `F3`: Switch between different crosshair colors (Red, Green, Blue).
    - `F4`, `F5`: Adjust the size of the crosshair (increase and decrease).
    - `F6`: Enter/Exit calibration mode to adjust the crosshair position using arrow keys.
    - `F7`: Reset the crosshair to its default settings (color, size, and position).
    - `F8`: Toggle the display of text prompts on the screen.
  - **Enhanced**: Improved the visibility of text prompts by adding a black border around the text and ensuring the text color dynamically adjusts to be visible against the background.
  - **Fixed**: Resolved an issue where the text prompts were not displaying correctly due to font rendering issues.
  - **Note**: The text prompts now have a black border for better visibility. The default text color is white, but it will change to black if the background is too bright.

---

## Hey there, gamers! Welcome to my little project! 🎉

This is a super-handy tool that lets you customize your crosshairs for different gaming scenarios. Whether you're using a shotgun, sniper rifle, RPG, or even a vehicle, you can easily switch between various crosshair styles with just a few key presses. Trust me, it’ll make your gaming experience way more fun! 😎

---

## What does it do?

- **Multiple Crosshair Styles**: Choose from different crosshair styles like Shotgun, SMG/Rifle/Sniper, RPG, Vehicle, and Custom. Each style is designed to fit specific gaming needs. 🎯  
- **Hotkey Switching**: Use the Page Up (Prior) and Page Down (Next) keys to quickly switch between crosshair styles. No need to pause your game or fiddle with settings! ⌨️  
- **Transparent Overlay**: The crosshair is displayed on a transparent window that stays on top of your game, so you can see it clearly without any distractions. 💡  

---

## How to Use It? 👇

### Getting Started:

1. Download the `Crosshair Customizer` files and make sure you have a Windows system. This tool is designed for Windows. 💻  
2. Inside the downloaded folder, you'll find the `./dist` directory. 📁  

### Running the Program:

1. Navigate to the `./dist` folder.  
2. Double-click `External_crosshair.exe` to run the program. (You might need to run it as an administrator. Right-click and select "Run as administrator.") 💥  
3. Once it’s running, you'll see a transparent crosshair on your screen. Use the Page Up (Prior) and Page Down (Next) keys to switch between different crosshair styles. 🎯  

### Customizing the Crosshairs:

Feel free to edit the `External_crosshair.py` file to add your own custom crosshair styles. Just follow the existing functions as a template and get creative! 🛠️

### How to Recompile? (Optional)

1. Make sure you have Python installed. (Python 3.8 or higher is recommended.) 🐍  
2. Install the required libraries:
   ```bash
   pip install pyinstaller
   ```
3. Compile the script using PyInstaller:
    ```bash
    pyinstaller --onefile --noconsole External_crosshair.py External_crosshair.py
    ```
4. The new External_crosshair.exe will be in the ./dist folder. Ready to go! 🚀

---

### Important Tips:
1. Game Compatibility: This tool is designed to enhance your gaming experience, but always check your game’s rules to ensure it’s allowed. Use it responsibly! 🙏
2. Admin Rights: Running the program as an administrator is a good idea to avoid any hiccups. 💪
3. Exiting the Program: To close the program, simply close the Python terminal or command prompt window, or press Ctrl+C. Easy peasy! 👋
    ```

### Project Structure:
```
准星/
├── MIT File
├── External_crosshair.py                         # The source code (If you want to tweak settings)
└── README.md                       # This file you’re reading right now!
```

---

### Want to Contribute? 🤝
Got ideas for new crosshair styles or improvements? Feel free to open an issue or submit a pull request! Let’s make this tool even better together! 🤝

---

### Contact Me：
Got questions or just want to chat? Hit me up via email! 📧
My email is: [lixinhe3465@163.com]
I'm still a student, so my response time might vary, but I'll do my best to get back to you as soon as possible. Remember to mention the purpose in the subject line! 😊

---

### Hope you enjoy this tool! Happy gaming, have fun in all of game! 😎
