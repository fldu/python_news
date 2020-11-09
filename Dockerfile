FROM fedora:33
LABEL fldu <fldu@fldu.fr>
RUN dnf upgrade -y && \
    dnf install -y python python-devel python-pip && \
    dnf clean all
RUN mkdir /app
COPY requirements.txt /app
WORKDIR /app
RUN useradd -m python
RUN chown -R python. /app
USER python
RUN pip install -r /app/requirements.txt --user

COPY ./app /app

RUN python -m unittest -v 
ENTRYPOINT python python_news.py