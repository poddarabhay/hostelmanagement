@echo off
title Virtual Env for Hostel Management
cmd /k "python manage.py makemigrations & python manage.py migrate"
@echo on