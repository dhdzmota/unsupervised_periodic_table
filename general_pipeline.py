import subprocess

command_list = [
    'python src/data/download_data.py',
    'python src/data/process_data.py',
    'python src/data/prepare_data.py',
    'python src/model/model_mechanism.py',
]

for command in command_list:
    subprocess.run(command.split(' '))
