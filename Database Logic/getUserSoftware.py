import subprocess
import os

commands = ['Get-WmiObject -Class Win32_Product | Select-Object Name',
            'Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName',
            'wmic product get name']
output_file = 'mySoftwares.txt'

avoid_lines = ['Name', '----', 'DisplayName', '-----------']

if (os.path.exists(output_file)):
    os.remove(output_file)
    print("deleted old file")


def getUserSoftware():
    # Open the output file in append mode
    with open(output_file, 'a+') as file:
        # Iterate over the commands
        for command in commands:
            file.seek(0)
            existing_content = file.read()
            # Execute the command and capture the output
            result = subprocess.run(['powershell', '-Command', command], capture_output=True, text=True)
            # Check if the command was executed successfully
            if result.returncode == 0:
                # Remove empty lines from the output and append to the file
                lines = result.stdout.split('\n')
                for line in lines:
                    line = line.rstrip()
                    if (not line.isspace() and line not in existing_content and line not in avoid_lines):
                        file.write(line)
                        file.write("\n")
            else:
                print(f"Command execution failed with error:\n{result.stderr}")



    print(f"Successfully appended the outputs of the commands to {output_file}")