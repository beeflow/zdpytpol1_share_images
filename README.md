**(fake) Production**
1. copy `.env.dist` to `.env` and set all variables if needed
1. run z `docker-compose up`
There will be a new user automatically created with username `admin` and password `h98yt54y5rd`

If container with postgres will start after container with application, you need to start postgres first:
`docker-compose up -d postgres` and then` docker-compose up -d app`

**Remte storage**

Application is repared to work with Amazon S3. If you need a different storage, you need to modify the 
configuration in `settings.py` file. Please read the documentation on https://django-storages.readthedocs.io/en/latest/

**API Documentation**

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/e8a6586e6f59d07cbb3a)

**Development**
1. copy `.env.dist` to `.env` and set all variables 
1. copy `local_dist.py` to `local.py` in `share_images` folder.
1. run `pip -r requirements_devel.txt`

**Testing**

Before you send your code to remote repository, please run all test locally

```
$ safety check --full-report
$ black --check -l 120 --exclude=migrations --exclude=venv .
$ flake8 .
$ bandit -x tests,./venv/ -r .
$ isort --check-only --diff .
$ coverage run --omit="venv/*" --branch --source=. ./manage.py test
```

You can run this commands to fix some bugs from static code analysis:
```
$ black -l 120 --exclude=migrations --exclude=venv .
$ isort .
```
