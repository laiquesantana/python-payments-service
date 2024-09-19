Payment Gateway Integration with FastAPI
=============

This project integrates multiple payment gateways, including Iugu and paypal, into a FastAPI-based service. The integration allows creating payments, managing customers, and handling various payment methods such as credit cards, boleto, and more.

Pre-requisites
--------------

You need these installed locally:

* Docker
* Docker-compose

### Envs

Copy the contents of `env.sample` to `.env` and `.env.test` (never commit 
your `.env` or `.env.test`):

```bash
cp env.sample .env
cp env.test.sample .env.test
```

Attention: It's important that your `.env.test` have the `DATABASE_URL` 
*pointing to your test database*, otherwise it won't be able to run migrations.

### Build docker image

```bash
docker-compose build app
```

You can access swagger documentation in localhost:2023/core/docs
### Databases

Create development and test databases

```bash
docker-compose run db sh -c "PGPASSWORD=root psql -U root -h fastapi_base_db -c 'drop database fastapi_base_development'"
docker-compose run db sh -c "PGPASSWORD=root psql -U root -h fastapi_base_db -c 'drop database fastapi_base_test'"
docker-compose run db sh -c "PGPASSWORD=root psql -U root -h fastapi_base_db -c 'create database fastapi_base_development'"
docker-compose run db sh -c "PGPASSWORD=root psql -U root -h fastapi_base_db -c 'create database fastapi_base_test'"
```

### Initial Migrations

You need to run all migrations

```bash
docker-compose run app bash -c "APP_ENV=development alembic upgrade head"
docker-compose run app bash -c "APP_ENV=test alembic upgrade head"
```

or, you can run with a single command

```bash
docker-compose run app bash -c "alembic upgrade head && APP_ENV=test alembic upgrade head"
```

How To 
------

### run

```bash
docker-compose up db app
```

### debug

```python
import pdb; pdb.set_trace()
```

### add new migration

```bash
docker-compose run app alembic revision -m "create order_payment"
```

### run migrations

```bash
docker-compose run app bash -c "alembic upgrade head && APP_ENV=test alembic upgrade head"
```


or to downgrade:

```bash
docker-compose run app bash -c "alembic downgrade -1 && APP_ENV=test alembic downgrade -1"
```

Test
----

### Configuration

First configure your environment variables:

```bash
cp env.sample .env.test
```

And change the value of `APP_ENV` and `DATABASE_URL` to:

```env
APP_ENV=test
DATABASE_URL=postgresql+asyncpg://root:root@fastapi_base_db/fastapi_base_test
```

### Run tests

```bash
docker-compose run app pytest tests
```

or just controllers tests:

```bash
docker-compose run app pytest tests/controller
```

or just models tests:

```bash
docker-compose run app pytest tests/model
```

or with detailed params

```bash
docker-compose run app pytest -v -s -rw tests --ignore-glob=*/controller/*
```

Deploy
------

Just push/merge to master.

### pyenv

Aws cli uses python, so it's better to create an isolated enviroment pyenv +  
pyenv-virtualenv

To install it on linux:

```bash
apt-get update
apt-get install build-essential libssl-dev libffi-dev python-dev
apt install python3-pip
pip3 install virtualenv  
```

To create your virtualenv with python 3.10.4:

```bash
python3 -m venv .venv
. .venv/bin/activate
```

Now virtualenv will auto activate and deactivate your env upon entering  
project folder.

# VS-Code

For developers using VS-code as a text editor, some facilities can be instantiated and used when requirements.dev.txt:

* integrated extension-> Black 
* integrated extension-> Isort 
* integrated extension-> autoDostring 
* integrated extension-> Pylint 
* integrated extension-> MyPy 
* integrated extension-> Flake8 
* integrated extension-> TodoTree 

For active some extensions add this sections to .vscode settings.json

```json
{
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        },
    },
    "isort.args": [
        "--profile",
        "black"
    ],
    "python.analysis.typeCheckingMode": "off",
    "python.linting.pylintEnabled": true,
    "python.linting.enabled": true,
    "editor.formatOnSave": true,
    "python.linting.flake8Enabled": false,
}
```


# Linters

This project contains configuration files for the following linters:

* [Bandit](https://bandit.readthedocs.io/en/latest/) ( segurança)
* [Black](https://black.readthedocs.io/en/stable/) (verificação estilística)
* [Isort](https://pycqa.github.io/isort/) (verificação estilística dos imports)
* [MyPy](https://mypy.readthedocs.io/en/stable/) (verificação da tipagem estática)
* [Flake8](https://flake8.pycqa.org/en/stable/) (básica: verificação estilística e logica)
* [Pylint](https://pylint.readthedocs.io/en/stable/) (complexa: verificação estilística e logica)

 See [linters-example.md](./linters-example.md) for more details to run:

# Anotations

List the notes made, and the behavior they can influence in each linter/process

* pylint
    * `# unused: used in verify_basic_auth`
    * `# pylint: disable=C0413`

* mypy
    * `# type: ignore`
# Pre-commit

To check pre-commit, run:

```bash
pre-commit run --all-files
```