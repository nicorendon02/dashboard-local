@echo off
start cmd /k python api.py
start cmd /k python DataManager.py
start cmd /k ng serve --host 192.168.0.100
