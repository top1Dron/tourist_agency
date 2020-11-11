# Dockerfile
FROM python:3.9
# RUN pip install pipenv
RUN mkdir /code
WORKDIR /code
# COPY Pipfile* /code/
RUN pip install -r ../requirements.txt
# RUN pipenv install --system --deploy --ignore-pipfile
ADD config /code/