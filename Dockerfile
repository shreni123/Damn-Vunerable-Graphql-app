FROM python:3.7-alpine

LABEL description="Damn Vunerable GraphqL app"
LABEL github="https://github.com/shreni123/Damn-Vunerable-Graphql-app"
LABEL maintainers="Shreni"

ARG TARGET_FOLDER=/opt/dvga1
WORKDIR $TARGET_FOLDER/

RUN apk add --update curl

COPY requirements.txt /opt/dvga1/
RUN pip install -r requirements.txt

ADD core /opt/dvga1/core
ADD db /opt/dvga1/db
ADD static /opt/dvga1/static
ADD templates /opt/dvga1/templates

COPY app.py /opt/dvga1
COPY config.py /opt/dvga1
COPY setup.py /opt/dvga1/
COPY version.py /opt/dvga1/

RUN python setup.py

EXPOSE 5000/tcp
CMD ["python3", "app.py"]
