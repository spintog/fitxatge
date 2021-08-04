import platform
from pathlib import Path

# Base settings
system = platform.system()

# Define config directory based on user's operating system
if system == 'Linux':
    conf_dir = Path.home().joinpath(".config/Microblau/Fitxatge")
elif system == 'Windows':
    conf_dir = Path.home().joinpath("AppData/Local/Microblau/Fitxatge")

# Define and verify if db_file exists
database_file = conf_dir.joinpath('fitxatge.db2')

# define and verify program dirs
gui_dir = Path('.').joinpath('gui')
img_dir = Path('.').joinpath('images')
