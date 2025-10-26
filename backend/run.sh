#!/bin/bash

# Carrega as variáveis de ambiente, o ambiente virtual, e executa o programa python

export $(grep -v '^#' .env | xargs) && source .venv/bin/activate && python3 main.py