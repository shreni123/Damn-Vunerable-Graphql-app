FROM python:3.7-alpine

LABEL description="Damn Vunerable Graphql app"
LABEL github="https://github.com/shreni123/Damn-Vunerable-Graphql-app"
LABEL maintainers="Shreni"

ARG TARGET_FOLDER=/opt/dvga
WORKDIR $TARGET_FOLDER/

RUN apk add --update curl

COPY requirements.txt /opt/dvga/
RUN pip install -r requirements.txt

ADD core /opt/dvga/core
ADD db /opt/dvga/db
ADD static /opt/dvga/static
ADD templates /opt/dvga/templates

COPY app.py /opt/dvga
COPY config.py /opt/dvga
COPY setup.py /opt/dvga/
COPY version.py /opt/dvga/

RUN python setup.py

EXPOSE 5000/tcp
CMD ["python3", "app.py"]
