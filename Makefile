.PHONY: setup \
		run \
		black \
		help

PIP_VERSION = 22.3.1

venv/bin/activate: ## Alias for virtual environment
	python -m venv venv

setup: venv/bin/activate ## Project setup
	. venv/bin/activate; pip install pip==${PIP_VERSION} wheel setuptools
	. venv/bin/activate; pip install --exists-action w -Ur requirements.txt
	cp .env.example .env

messenger: venv/bin/activate ## Local Run Messenger
	. venv/bin/activate; python messenger.py

server: venv/bin/activate ## Local Run Server
	. venv/bin/activate; python server.py

file_to_black = .
black: venv/bin/activate ## Run black
	. venv/bin/activate; black $(file_to_black)
