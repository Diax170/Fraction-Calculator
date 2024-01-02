# Fraction Calculator
A fraction caclulator, made in Python. It can:
- Forward fractions
- Extract wholes
- Convert fractions to improper
- Extend fractions
- Bring fractions to common denominator

There is also an eval calculator included.

# Setup
You can run the executable for Windows (releases) or open main.py if you have installed Python 3.

# Bundling a new executable
Feel free to use my code, but mention that I made the original.
How to bundle a new executable:
1. Move script files and icon.ico to one directory.
2. Navigate to that directory using CMD.
3. Make sure that you have installed Python and pyinstaller; you can get Python from https://python.org, pyinstaller is downloaded via 'pip install pyinstaller' command (if it doesn't work, replace pip with pip3).
4. Type the following command: pyinstaller -F main.py -w -i icon.ico
5. The executable should be located in a new 'dist' folder.
