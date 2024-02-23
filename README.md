# Windows/MacOS install

1. If you are using PyCharm - it may propose you to automatically create venv for your project 
    and install requirements in it, but if not:

    `python -m venv venv`

    `venv\Scripts\activate` (on Windows)

    `source venv/bin/activate` (on macOS)

    `pip install -r requirements.txt`

# Requirements:

1. The presence of the Chrome Browser on the device

# Сustomization of the parsing process

### You can change parsing settings using the config.json file:

- "PROCESSED_FILES_DIR" is an option to change the final folder for csv storage
- "SEMIFINISHED_FILES_DIR" is an option to change the intermediate folder for storing csv
- "RAW_DATA_PATH" is an option to select the file from which the data will be taken
- "ADDITIONAL_FACEBOOK_PARSING" is an option to enable/disable additional Facebook parsing (double the script running time)
- "CLEAN_SEMIFINISHED_FILES_DIR" is an option for pre-cleaning the folder in which intermediate files will be stored()
- "CLEAN_PROCESSED_FILES_DIR" is an option for pre-cleaning the folder in which the final files will be stored

# Pay attention:

- ALL files located in the semi-finished folder (by default) will be parsed
- files with identical names will be overwritten (file names are equal to sheet names)
- 