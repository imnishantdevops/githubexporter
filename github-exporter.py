#!/usr/bin/env python3

from datetime import datetime, timedelta
import time
from prometheus_client import start_http_server, Counter
from github import Github

# TODO: move to env vars
import os

github_token = os.environ.get("GITHUB_TOKEN")
github_token = "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"

# to get PRs closed during last N days
days_ago = datetime.now() - timedelta(days=7)
# buckets for PRs closed during {interval}
time_intervals = [1, 2, 5, 10, 20, 50, 100, 1000]  # 1 hour, 2 hours, 5 hours
# prometheus metric to count PRs in each {interval}
pull_request_duration_count = Counter('pull_request_duration_count',
                                      'Count of Pull Requests within a time interval',
                                      labelnames=['repo_name', 'time_interval'])

def calculate_pull_request_duration(repository, pr):
    created_at = pr.created_at
    merged_at = pr.merged_at

    if created_at >= days_ago and created_at and merged_at:
        duration = (merged_at - created_at).total_seconds() / 3600

        # Increment the Counter for each time interval
        for interval in time_intervals:
            if duration <= interval:
                print(f"PR ID: {pr.number} Duration: {duration} Interval: {interval}")
                pull_request_duration_count.labels(time_interval=interval, repo_name=repository).inc()
                break

def main():
    # connect to Github
    github_instance = Github(github_token)
    # specify your personal GitHub username
    github_username = 'imnishantdevops'

    # get repos list
    repositories = github_instance.get_user(github_username).get_repos()

    for repository in repositories:
        # to set in labels
        repository_name = repository.full_name.split('/')[1]
        pull_requests = repository.get_pulls(state='closed')

        if pull_requests.totalCount > 0:
            print(f"Checking repository: {repository_name}")
            for pr in pull_requests:
                calculate_pull_request_duration(repository_name, pr)
        else:
            print(f"Skipping repository: {repository_name}")

    # Start Prometheus HTTP server
    start_http_server(8000)
    print("HTTP server started")
    while True:
        time.sleep(15)
        pass
if __name__ == '__main__':
    main()
