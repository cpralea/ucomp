import argparse

from typing import List

from tvm import *


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Test the VM assembler.')
    parser.add_argument('--root', metavar='ROOT', type=str, dest='root_dir', \
                        required=False, default='tests', \
                        help='root directory for in/asm/*.vmasm and in/ref/asm/*.{hex,lbl}')
    return parser.parse_args()


def execute_test(name: str, in_vmasm: str, ref_hex: str, ref_lbl: str, out_hex: str, out_lbl: str):
    print(f"{name}...", end='')

    if not execute(f"python3 $UCOMP_DEVROOT/tools/vmasm.py -o {out_hex} -l {out_lbl} {in_vmasm}"):
        print_red('failed')
        return
    if not (execute(f"diff {ref_hex} {out_hex}") and execute(f"diff {ref_lbl} {out_lbl}")):
        print_red('failed')
        return
    
    print_green('pass')


def execute_tests():
    args: argparse.Namespace = parse_args()

    in_dir: str                             = f"{args.root_dir}/in/asm"
    ref_dir: str                            = f"{args.root_dir}/ref/asm"
    out_dir: str                            = create_tmpdir('vmasm2hex-')

    names: List[str]                        = [f"{file.rpartition('.')[0]}" for file in list_files(in_dir, '.vmasm')]
    in_vmasm_files: List[str]               = [f"{in_dir}/{name}.vmasm" for name in names]
    ref_hex_files: List[str]                = [f"{ref_dir}/{name}.hex" for name in names]
    ref_lbl_files: List[str]                = [f"{ref_dir}/{name}.lbl" for name in names]
    out_hex_files: List[str]                = [f"{out_dir}/{name}.hex" for name in names]
    out_lbl_files: List[str]                = [f"{out_dir}/{name}.lbl" for name in names]

    tests: zip[tuple[str, str, str, str, str, str]] \
        = zip(names, in_vmasm_files, ref_hex_files, ref_lbl_files, out_hex_files, out_lbl_files)

    print_green("*.vmasm -> *.{hex,lbl}")
    for name, in_vmasm, ref_hex, ref_lbl, out_hex, out_lbl in tests:
        execute_test(name, in_vmasm, ref_hex, ref_lbl, out_hex, out_lbl)
    
    remove_dir(out_dir)


execute_tests()
