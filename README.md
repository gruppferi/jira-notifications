[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
![Static Badge](https://img.shields.io/badge/docstring-codiumate-%3F?color=blue)

# jira-notifications

Jira Notifications is a Python package that leverages system D-Bus using the `notify` package to send system toast notifications about new tickets in Jira. It allows users to configure the period for checking new tickets and also sends a daily notification about newly created tickets at a specified time.

## Installation

You can install Jira Notifications via pip:

```
pip install jira-notifications
```
## Usage

After installation, you can use the `jira-notifications` command to generate sample config, update the yaml with correct information

```bash
jira-notifications -g jira.yaml
```
### Linux (Debian Based)
* The Linux version has feature that each ticket is clickable and opens that ticket on your browser

#### Make it run a system package
```
[Unit]
Description=jira-notifications Daemon
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/<username>
ExecStart=/home/<username>/.local/bin/jira_notifications -c /home/<username>/Documents/jira-config.yaml
Restart=always

[Install]
WantedBy=default.target


```

```
systemctl --user enable jira-notifications.service
systemctl --user start jira-notifications.service
systemctl --user status jira-notifications.service


```
### Windows (10, 11)
!!! MISSING
-> Any PR to fix the following issues would be highly welcome, since I am not windows guy  &#x1F612; &#x1F610; I tried alot, couldn't make following to work
* Basic test works the program runs and show toasts but each ticket is not clickable. clicking on toast opens the jira.
* No service, No like systemD in linux for windows to start automatically and run it forever.
It is highly appreciated if someone can create PR and fix the above two issues.
* Can not show more 6 lines on toast


## Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/. <br>
This project used Codiumate, for details see https://www.codium.ai/