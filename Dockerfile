FROM python:2.7.10
LABEL maintainer="Arthur Atrokhov <aatrokhov@gmail.com>"
ENV DJANGO_SETTINGS_MODULE freelance.settings
RUN pip install --upgrade pip
ADD requirements.txt /freelance/requirements.txt
RUN pip install -r /freelance/requirements.txt
ADD . /freelance
WORKDIR /freelance/