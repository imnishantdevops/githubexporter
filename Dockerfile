FROM python:3

COPY github-exporter.py ./
ENV GITHUB_TOKEN="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"
RUN pip install prometheus_client PyGithub

CMD [ "python", "./github-exporter.py"]
