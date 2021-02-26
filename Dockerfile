FROM python:3
RUN mkdir src/
COPY python-requirements.txt
WORKDIR /src/
RUN pip install -r python-requirements.txt
ADD . /src/ 