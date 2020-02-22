cd ./tests
coverage run -m --source="../src" pytest
coverage report -m
cd ../