# Examples to run linters

## Run black:
```bash
$ black ./app
```
## Run isort:
```bash
$ isort ./app/ --profile black
```

## Run bandit:
```bash
$ bandit --configfile bandit.yaml -r ./app
```

## Run MyPy:
```bash
$ mypy --config-file ./.mypy.ini ./app
```

## Run Flake8:
```bash
$ flake8 --config .flake8 ./app/
```

## Run Pylint:
```bash
$ pylint --rcfile=.pylintrc ./app/ --recursive y
```

## Run Docformatter:
```bash
$ docformatter --config tox.ini -e migrations -i -r .
```


