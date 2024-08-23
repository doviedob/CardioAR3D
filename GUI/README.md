# MONAI Label SSH Connector

This Python script provides a graphical user interface (GUI) for connecting to a remote server via SSH and managing a MONAI Label environment. It simplifies the process of activating a conda environment and starting a MONAI Label server on an EC2 instance. The application allows users to input the server's public IPv4 address, select a PEM file for authentication, and execute commands to set up and run MONAI Label.

![image](https://github.com/user-attachments/assets/edbd40f3-5b34-463c-ac81-a7b8b59b67d3)

***NOTE:*** You can create a .exe running this commands:

```
pip install pyinstaller
```

If you want create a .spec file, follow this command:
```
python -m PyInstaller --onefile -w main.py
```
Then, create the .exe file
```
python -m PyInstaller main.spec
```
Found the .exe on te folder ***dist***
## Key Features:
- Easy-to-use GUI for SSH connection and command execution
- Automatic conversion of IPv4 to EC2 hostname
- PEM file selection for secure authentication
- Step-by-step buttons for connecting, activating the environment, and starting the server
- Real-time output display

## Requirements:
- Python 3.x
- tkinter
- paramiko
- PIL (Python Imaging Library)

## Usage:
1. Clone the repository
2. Install the required dependencies: `pip install paramiko Pillow`
3. Run the script: `python main.py`
4. Enter the EC2 instance's public IPv4 address
5. Select the PEM file for authentication
6. Follow the on-screen buttons to connect and start the MONAI Label server

Note: Ensure you have the necessary permissions and have configured your EC2 instance to run MONAI Label before using this tool.

## Customization:
You can modify the MONAI Label start command in the `start_server` method to fit your specific dataset and model requirements.

## Contributing:
Contributions, issues, and feature requests are welcome. Feel free to check the issues page if you want to contribute.

## License:
[Insert your chosen license here]
