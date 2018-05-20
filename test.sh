#!/bin/bash

coverage run --branch --source=src -m unittest discover test
coverage report
coverage xml
