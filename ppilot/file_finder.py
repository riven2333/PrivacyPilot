import subprocess
import platform

def find_file(pattern, local_src_dir):

    if platform.system() == "Windows":
        cmd = f'cd /D "{local_src_dir}" && dir /s /b | findstr /R "{pattern}"'
    else:
        cmd = f'find "{local_src_dir}" -type f | grep -P "{pattern}"'
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        return result.stdout.decode().split('\n')
    else:
        return f"Cannot find the selected file {pattern} in {local_src_dir} \n{cmd}"

