.PHONY: venv all vm clean

all: vm

venv:
	python3 -m venv env/python

vm:
	make -C vm all

clean:
	make -C vm clean
