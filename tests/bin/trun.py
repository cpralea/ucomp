from utils import execute


execute('python3 $UCOMP_DEVROOT/tests/bin/tvmasm.py')
execute('python3 $UCOMP_DEVROOT/tests/bin/tvmdisasm.py')
execute('python3 $UCOMP_DEVROOT/tests/bin/tvmasmroundtrip.py')
