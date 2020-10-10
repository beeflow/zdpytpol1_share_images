# pull official base image
FROM python:3.8
RUN mkdir /code
WORKDIR /code

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# wait for postgres
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

COPY ./requirements.txt /code/
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# copy project
COPY app-entrypoint.sh /
CMD /wait
RUN chmod +x /app-entrypoint.sh

ENTRYPOINT ["/app-entrypoint.sh"]
