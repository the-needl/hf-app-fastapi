#Deriving the latest base image
FROM python:3.11.3-slim-bullseye

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME

RUN pip install poetry

COPY . ./

RUN apt-get update
RUN apt-get install ca-certificates
RUN apt-get install libpq-dev gcc build-essential wkhtmltopdf  -y 
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

RUN poetry install

# ARG OPENAI_API_KEY
# ENV OPENAI_API_KEY=$OPENAI_API_KEY

# CMD ["poetry", "run", "start"]
CMD ["serve", "run", "app.main:main"]