import argparse

from typing import List

from utils import *


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Test the VM disassembler.')
    parser.add_argument('--root', metavar='ROOT', type=str, dest='root_dir', \
                        required=False, default='tests', \
                        help='root directory for in/asm/*.{hex,lbl} and in/ref/asm/*.vmasm')
    return parser.parse_args()


def execute_test(name: str, in_hex: str, in_lbl: str, ref_vmasm: str, out_vmasm: str):
    print(f"{name}...", end='')

    if not execute(f"python3 $UCOMP_DEVROOT/tools/vmdisasm.py -o {out_vmasm} -l {in_lbl} {in_hex}"):
        print_red('failed')
        return
    if not execute(f"diff {ref_vmasm} {out_vmasm}"):
        print_red('failed')
        return
    
    print_green('pass')


def execute_tests():
    args: argparse.Namespace = parse_args()

    in_dir: str                             = f"{args.root_dir}/in/disasm"
    ref_dir: str                            = f"{args.root_dir}/ref/disasm"
    out_dir: str                            = create_tmpdir('vmdisasm2hex-')

    names: List[str]                        = [f"{file.rpartition('.')[0]}" for file in list_files(in_dir, '.hex')]
    in_hex_files: List[str]                 = [f"{in_dir}/{name}.hex" for name in names]
    in_lbl_files: List[str]                 = [f"{in_dir}/{name}.lbl" for name in names]
    ref_vmasm_files: List[str]              = [f"{ref_dir}/{name}.vmasm" for name in names]
    out_vmasm_files: List[str]              = [f"{out_dir}/{name}.vmasm" for name in names]

    tests: zip[tuple[str, str, str, str, str]] \
        = zip(names, in_hex_files, in_lbl_files, ref_vmasm_files, out_vmasm_files)

    print_green("*.{hex,lbl} -> *.vmasm")
    for name, in_hex, in_lbl, ref_vmasm, out_vmasm in tests:
        execute_test(name, in_hex, in_lbl, ref_vmasm, out_vmasm)
    
    remove_dir(out_dir)


execute_tests()
