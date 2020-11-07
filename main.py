import requests
import os
import json
import sys


def actionColor(status):
    """
    Get a action color based on the workflow status.
    """

    if status == 'success':
        return 'good'
    elif status == 'failure':
        return 'danger'

    return 'warning'


def actionStatus(status):
    """
    Get a transformed status based on the workflow status.
    """

    if status == 'success':
        return 'SUCCESS'
    elif status == 'failure':
        return 'FAILED'

    return 'WARNING'


def actionEmoji(status):
    """
    Get an emoji based on the workflow status.
    """

    if status == 'success':
        return ':heavy_check_mark:'
    elif status == 'failure':
        return ':x:'

    return ':zipper_mouth_face:'


def notify_slack(job_status, notify_when):
    url = os.getenv('SLACK_WEBHOOK_URL')
    workflow = os.getenv('GITHUB_WORKFLOW')
    repo = os.getenv('GITHUB_REPOSITORY')
    branch = os.getenv('GITHUB_REF')
    commit = os.getenv('GITHUB_SHA')

    commit_url = f'https://github.com/{repo}/commit/{commit}'
    repo_url = f'https://github.com/{repo}/tree/{branch}'

    color = actionColor(job_status)
    status_message = actionStatus(job_status)
    emoji = actionEmoji(job_status)

    pretext = f'<{repo_url}|{repo} ({branch})>'
    text = f'{emoji} {workflow}\n\n*• Status*: {status_message}\n• *Commit*: <{commit_url}|{commit[:7]}>'
    fallback = f'{workflow} {status_message} {repo_url}'

    payload = {
        'username': 'Github Action',
        'icon_emoji': ':octocat:',
        'attachments': [
            {
                'text': text,
                'fallback': fallback,
                'pretext': pretext,
                'color': color,
                'mrkdwn_in': ['text'],
                'footer': 'By <https://github.com/asomas/notify-slack-action|asomas/notify-slack-action>',
            }
        ]
    }

    payload = json.dumps(payload)

    headers = {'Content-Type': 'application/json'}

    if notify_when is None:
        notify_when = 'success,failure,warnings'

    if job_status in notify_when and not testing:
        requests.post(url, data=payload, headers=headers)


def main():
    job_status = os.getenv('INPUT_STATUS')
    notify_when = os.getenv('INPUT_NOTIFY_WHEN')
    notify_slack(job_status, notify_when)


if __name__ == '__main__':
    try:
        testing = True if sys.argv[1] == '--test' else False
    except IndexError as e:
        testing = False

    main()
