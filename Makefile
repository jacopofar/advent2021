# shamelessly copied from https://github.com/venthur/blag/blob/master/Makefile
PY = python3
VENV = .venv
BIN=$(VENV)/bin


ifeq ($(OS), Windows_NT)
	BIN=$(VENV)/Scripts
	PY=python
endif


all: mypy lint test
$(VENV): requirements.txt
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --upgrade -r requirements.txt
	touch $(VENV)

format: $(VENV)
	$(BIN)/black -l 80 advent2021

mypy: $(VENV)
	$(BIN)/mypy advent2021