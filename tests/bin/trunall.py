from utils import execute


execute('python3 $UCOMP_DEVROOT/tests/bin/tasm.py')
execute('python3 $UCOMP_DEVROOT/tests/bin/tdisasm.py')
execute('python3 $UCOMP_DEVROOT/tests/bin/tasmroundtrip.py')
execute('python3 $UCOMP_DEVROOT/tests/bin/tvm.py')
