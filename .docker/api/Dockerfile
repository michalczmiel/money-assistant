FROM python:3.7.3 AS base
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y upgrade

WORKDIR /api

RUN pip install --upgrade pip

COPY requirements.txt requirements_dev.txt ./

RUN pip install -r requirements_dev.txt

FROM base AS dev

COPY .docker/api/entrypoint-dev.sh /usr/local/bin/
RUN chmod a+x /usr/local/bin/entrypoint-dev.sh

CMD ["/usr/local/bin/entrypoint-dev.sh"]

FROM base as prod

COPY .docker/api/entrypoint.sh /usr/local/bin/
RUN chmod a+x /usr/local/bin/entrypoint.sh

COPY . /api/

ENTRYPOINT ["entrypoint.sh"]
