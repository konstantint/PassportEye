del /Q dist\*.tar.gz
python setup.py sdist && twine upload dist\*.tar.gz
