import platform
from pathlib import Path

# Base settings
system = platform.system()
base_dir = Path.cwd()

# Define config directory based on user's operating system
if system == 'Linux':
    conf_dir = Path.home().joinpath('.config/Microblau/Fitxatge')
elif system == 'Windows':
    conf_dir = Path.home().joinpath('AppData/Local/Microblau/Fitxatge')
conf_dir.mkdir(parents=True, exist_ok=True)

# Define and verify if db_file exists
database_file = conf_dir.joinpath('fitxatge.db')

# define and verify program dirs
gui_dir = Path(base_dir).joinpath('gui')
img_dir = Path(base_dir).joinpath('images')
