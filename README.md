# BL4 Save Duplicator

A simple GUI application to duplicate BL4 save files.

## Download
There are 2 ways to use this application:
- Download the latest Windows executable [here](https://github.com/Judgy53/BL4_Save_Duplicator/releases/latest)
- Clone the repo and run from source (see [Development](#Development))

## Usage

![](https://raw.githubusercontent.com/Judgy53/BL4_Save_Duplicator/refs/heads/main/assets/example.png)

0. <b>MAKE BACKUPS BEFORE DOING ANYTHING TO YOUR SAVES.</b>
1. Select the save you want to duplicate.
2. Enter your steam id. If the save is located where the game usually stores it, it should get automatically detected.
    Not sure if Epic Game Store saves work, I don't have a way to test it.
3. Modify your duplicated save as you like. 2 small warnings:
    - You probably want to keep `Randomize character GUID` checked. Otherwise, the game might confuse the duplicated save with the original, and weird stuff will happen.
    - `Reset challenges` and `Reset UVH Challenges` are experimental and not really tested. Use with caution.
4. Click on `Duplicate Save File` and enter a new file name. The file name must only contain hexadecimal characters (0-9, A-F) to be recognized by the game.
5. If the game is running, the save will appear but might not load. If that's the case, simply return to title screen to force it to reload everything (faster than restarting the game).
6. Enjoy !

## Development

### Requirements
- Python 3.8+

### Installation
1. Clone the repo:
    ```sh
    git clone https://github.com/Judgy53/BL4_Save_Duplicator/
    ```
2. Create a virtual environment (optional but recommended):
    ```sh
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
3. Install requirements:
    ```sh
    pip install -r requirements.txt
    ```
4. Run the app:
    ```sh
    python .\src\main.py
    ```

### Packaging
1. Install build requirements:
    ```sh
    pip install -r requirements.build.txt
    ```
2. Start the build:
     ```sh
    .\build.bat
    ```
    The exe will be created at `dist\BL4 Save Duplicator.exe`.

## Credits
- glacierpierce's [blcrypt](https://github.com/glacierpiece/borderlands-4-save-utility) for reading and writing save files.
