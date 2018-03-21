@echo off
title Virtual Env for Hostel Management
cmd /k "python manage.py migrate --run-syncdb"
@echo on