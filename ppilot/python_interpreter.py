import ast
import os
import subprocess
import sys
import tempfile


def log_print(log: str, result: dict = None, level: str = "INFO"):
    log_str = f"[{level}] {log}"
    print(log_str)
    if result is not None:
        result["logs"] += "\n" + log_str


def extract_imports(code):
    tree = ast.parse(code)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module)
    return imports


def is_installable(package_name):
    try:
        result = subprocess.run(['pip', 'install', package_name, '--dry-run'], capture_output=True, text=True)
        return 'ERROR' not in result.stderr
    except Exception:
        return False


def filter_installable_packages(modules):
    installable_modules = set()
    for module in modules:
        if is_installable(module):
            installable_modules.add(module)
    return installable_modules


def create_requirements_file(imports, filepath='temp_requirements.txt'):
    with open(filepath, 'w') as f:
        for package in imports:
            f.write(f"{package}\n")


def create_virtual_env(temp_dir):
    venv_dir = os.path.join(temp_dir, 'temp_venv')
    subprocess.run([sys.executable, '-m', 'venv', venv_dir], check=True)
    return venv_dir


def install_packages(venv_dir, packages):
    pip_executable = os.path.join(venv_dir, 'bin', 'pip') if os.name != 'nt' else os.path.join(venv_dir, 'Scripts', 'pip.exe')
    subprocess.run([pip_executable, 'install'] + packages, check=True)


def run_code_in_venv(venv_dir, code):
    python_executable = os.path.join(venv_dir, 'bin', 'python') if os.name != 'nt' else os.path.join(venv_dir, 'Scripts', 'python.exe')
    process = subprocess.run([python_executable, '-c', code], capture_output=True, text=True)
    return process.stdout, process.stderr


def python_interpreter(code):
    result = {"status": "", "stdout": "", "stderr": "", "logs": ""}
    imports = extract_imports(code)
    imports = list(imports)
    log_print("Imported Modules:" + str(imports), result=result)
    installable_modules = filter_installable_packages(imports)
    installable_modules = list(installable_modules)
    log_print("Installable Modules:" + str(installable_modules), result=result)
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            venv_dir = create_virtual_env(temp_dir)
            log_print(f"venv_dir: {venv_dir}", result=result)
            install_packages(venv_dir, installable_modules)
            result["stdout"], result["stderr"] = run_code_in_venv(venv_dir, code)
            result["status"] = "success"
        except Exception as e:
            log_print(str(e), result=result, level="ERROR")
            result["status"] = "failed"
    return result
