FROM 'frolvlad/alpine-python3'
MAINTAINER Bohdan Horbeshko <bodqhrohro@gmail.com>

ENV INSTALL_PATH /book_api
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . .

RUN python -c 'from book_api.app import init_database; init_database()'

CMD gunicorn -b 0.0.0.0:8001 --access-logfile - "book_api.app:app"
