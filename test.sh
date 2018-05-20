#!/bin/bash

coverage run --source=src -m unittest discover test
coverage report
coverage xml
