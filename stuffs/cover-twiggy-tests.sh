#!/bin/bash
python-coverage -e
python-coverage -o /usr -x  `which unit2` discover
python-coverage -o /usr -r -m `find twiggy -name "*.py"`
