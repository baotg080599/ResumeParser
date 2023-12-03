FROM ubuntu

# set work directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN apt-get update

RUN apt-get install -y python3-pip
RUN pip3 install -r /usr/src/app/requirements.txt
RUN python3 -m spacy download en_core_web_sm
RUN python3 -m nltk.downloader words
RUN python3 -m nltk.downloader stopwords
RUN pip3 install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz
RUN python3 /usr/src/app/pre_requisites.py
RUN python3 /usr/src/app/manage.py migrate
RUN python3 /usr/src/app/manage.py collectstatic --no-input