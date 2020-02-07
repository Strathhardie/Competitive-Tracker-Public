# Change-Auditor

A Web Scraper application to automate the compilation of interest rate data from various competitor websites. This repository specifically detects if the HTML of a website has changed since the last run.

## How to clone & connect to this repository

1. On Git Bash, configure the Proxy settings by entering this command. The port may be different depending on CNTLM settings. Ensure the proxy is running (ie. CNTLM.exe):
`` git config --global http.proxy "127.0.0.1:5128" `` 

2. Create a personal access token by following this guide. Use it as your password for authentication instead: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/

- The SSH port 22 seems to be blocked by the firewall, so clone using HTTPS.

- You can update your Git credentials if it is saved by going to Control Panel > Credential Manager > Windows Credentials > Generic Credentials > git:https://github.cibcdevops.com

## How to install the dependencies

Ensure you have Python 3.6 or higher installed.

1. After cloning this repository, open it on your terminal and run:

`` pip install resources/selenium-3.13.0-py2.py3-none-any.whl ``

`` pip install resources/PyYAML-3.13-cp36-cp36m-win_amd64.whl ``

## How to run the Change-Auditor (source code)

1. Open the repo on your terminal and run:
`` python main.py ``

Note: You may have to lower your bit9 settings to run resources/chromedriver.exe

## How to run the change-checker (executable release)

1. Unzip [feature/change-auditor-executable](executables/lastest_build)
2. Run main/main.exe

Note: You may have to lower your bit9 settings to run main.exe

## Development Workflow
We will be using the Git Flow Workflow. In this workflow, all code is committed to a `feature/feature-name` branch, reviewed, and merged to `master` for deployment. Find out more [here](https://guides.github.com/introduction/flow/) and [here.](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

```git
git checkout develop
git flow feature start my-feature
git commit -m "This is a change"
.
.
git commit -m "This is my last change for the feature"
git flow feature finish my-feature
```

### Issues:
The project backlog issues are tagged accordingly so they can be filtered out when viewing the issues page, as we do not have the GitHub Kanban Project board available.
When taking on a backlog item, remove the `Not Now/Backlog` label and assign the `NOW` label, then assign the issue yourself or the individual who will work on it.
**Backlog items should never be assigned without changing the tag and should never change the tag without assigning the item.** This can be critical to ensuring that everyone can see what is being worked on and what is not being worked on within the issues view.
