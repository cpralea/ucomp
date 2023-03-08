import argparse

from typing import List

from utils import *


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Test the VM.')
    parser.add_argument('--root', metavar='ROOT', type=str, dest='root_dir', \
                        required=False, default='tests', \
                        help='root directory for in/vm/*.asm and in/ref/vm/*.stdout')
    return parser.parse_args()


def execute_test(name: str, in_asm: str, ref_stdout: str, out_hex: str, out_stdout: str):
    print(f"{name}...", end='')

    if not execute(f"python3 $UCOMP_DEVROOT/tools/asm.py -o {out_hex} {in_asm}"):
        print_red('failed')
        return
    if not execute(f"source env.sh && python3 $UCOMP_DEVROOT/tools/vm.py {out_hex} > {out_stdout}"):
        print_red('failed')
        return
    if not execute(f"diff {ref_stdout} {out_stdout}"):
        print_red('failed')
        return

    print_green('pass')


def execute_tests():
    args: argparse.Namespace = parse_args()

    in_dir: str                             = f"{args.root_dir}/in/vm"
    ref_dir: str                            = f"{args.root_dir}/ref/vm"
    out_dir: str                            = create_tmpdir('asm2stdout-')

    names: List[str]                        = [f"{file.rpartition('.')[0]}" for file in list_files(in_dir, '.asm')]
    in_asm_files: List[str]                 = [f"{in_dir}/{name}.asm" for name in names]
    ref_stdout_files: List[str]             = [f"{ref_dir}/{name}.stdout" for name in names]
    out_hex_files: List[str]                = [f"{out_dir}/{name}.hex" for name in names]
    out_stdout_files: List[str]             = [f"{out_dir}/{name}.stdout" for name in names]

    tests: zip[tuple[str, str, str, str, str]] \
        = zip(names, in_asm_files, ref_stdout_files, out_hex_files, out_stdout_files)

    print_green("*.asm -> *.stdout")
    for name, in_asm, ref_stdout, out_hex, out_stdout in tests:
        execute_test(name, in_asm, ref_stdout, out_hex, out_stdout)
    
    remove_dir(out_dir)


execute_tests()
