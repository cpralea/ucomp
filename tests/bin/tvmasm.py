import argparse
import os
import shutil
import subprocess
import tempfile

from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Test the VM assembler.')
    parser.add_argument('--root', metavar='ROOT', type=str, dest='root_dir', \
                        required=False, default='tests', \
                        help='root directory for in/asm/*.vmasm and in/ref/asm/*.out')
    return parser.parse_args()


def list_files(dir_name: str, file_suffix: str) -> List[str]:
    return [file for file in os.listdir(dir_name) if file.endswith(file_suffix)]


def create_tmpdir(dir_prefix: str) -> str:
    return tempfile.mkdtemp(prefix=dir_prefix)


def remove_dir(dir_name: str):
    shutil.rmtree(dir_name, ignore_errors=True)


def print_red(msg: str, end: str | None = None):
    print(f"\033[91m{msg}\033[0m", end=end)
def print_green(msg: str, end: str | None = None):
    print(f"\033[92m{msg}\033[0m", end=end)


def execute(cmd: str) -> bool:
    process = subprocess.run(cmd, shell=True)
    return True if process.returncode == 0 else False


def execute_test(name: str, asm_file: str, ref_file: str, hex_file: str):
    print(f"{name}...", end='')

    if not execute(f"python3 $UCOMP_DEVROOT/tools/vmasm.py -o {hex_file} {asm_file}"):
        print_red('failed')
        return
    if not execute(f"diff {ref_file} {hex_file}"):
        print_red('failed')
        return
    
    print_green('pass')


def execute_tests():
    args: argparse.Namespace = parse_args()

    asm_dir: str                            = f"{args.root_dir}/in/asm"
    ref_dir: str                            = f"{args.root_dir}/ref/asm"
    hex_dir: str                            = create_tmpdir('vmasm2hex-')

    names: List[str]                        = [f"{file.rpartition('.')[0]}" for file in list_files(asm_dir, '.vmasm')]
    asm_files: List[str]                    = [f"{asm_dir}/{name}.vmasm" for name in names]
    ref_files: List[str]                    = [f"{ref_dir}/{name}.ref" for name in names]
    hex_files: List[str]                    = [f"{hex_dir}/{name}.hex" for name in names]

    tests: zip[tuple[str, str, str, str]]   = zip(names, asm_files, ref_files, hex_files)

    for name, asm_file, ref_file, hex_file in tests:
        execute_test(name, asm_file, ref_file, hex_file)
    
    remove_dir(hex_dir)


execute_tests()
