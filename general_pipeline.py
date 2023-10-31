import subprocess

command_list = [
    'python src/data/download_data.py',
    'python src/data/clean_data.py',
]

for command in command_list:
    subprocess.run(command.split(' '))
