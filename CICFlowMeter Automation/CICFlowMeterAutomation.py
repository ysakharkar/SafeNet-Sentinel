import subprocess
import time
from pywinauto import Application

# Path to the Windows batch file
batch_file = r'C:\Users\arcad\Downloads\drive-download-20230623T213527Z-001\bin\CICFlowMeter.bat'

# Launch Cicflowmeter in a new command prompt window
process = subprocess.Popen(["start", "cmd", "/k", batch_file], shell=True)

# Wait for Cicflowmeter window to appear
time.sleep(5)  # Adjust the delay as needed

# Connect to the Cicflowmeter window using Pywinauto
app = Application(backend="uia").connect(title="CICFlowMeter")  # Update with the appropriate window title

# Get the main window of Cicflowmeter
main_window = app.window(title="CICFlowMeter")  # Update with the appropriate window title