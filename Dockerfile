FROM python:3

COPY github-exporter.py ./
RUN pip install prometheus_client PyGithub

CMD [ "python", "./github-exporter.py"]
