FROM python:3.7.3 AS base
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y upgrade

WORKDIR /worker

RUN pip install --upgrade pip

COPY requirements.txt requirements_dev.txt ./

RUN pip install -r requirements_dev.txt

COPY .docker/worker/entrypoint.sh /usr/local/bin/
RUN chmod a+x /usr/local/bin/entrypoint.sh

FROM base AS dev

CMD ["/usr/local/bin/entrypoint.sh"]

FROM base AS prod

COPY . /worker/

ENTRYPOINT ["entrypoint.sh"]
