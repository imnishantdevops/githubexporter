FROM python:3

COPY github-exporter.py ./
ENV GITHUB_TOKEN="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"
RUN pip install prometheus_client PyGithub

CMD [ "python", "./github-exporter.py"]
