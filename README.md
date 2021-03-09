# Change-Auditor

A Web Scraper application to automate the compilation of interest rate data from various competitor websites. This repository specifically detects if the HTML of a website has changed since the last run.

## How to clone & connect to this repository

Create a personal access token by following this guide. Use it as your password for authentication instead: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/

- The SSH port 22 seems to be blocked by the firewall, so clone using HTTPS or GitHub CLI when using the public repo.

- You can update your Git credentials if it is saved by going to Control Panel > Credential Manager > Windows Credentials > Generic Credentials > git:https://github.cibcdevops.com

## How to install the dependencies

Ensure you have Python 3.6 or higher installed.

1. After cloning this repository, open it on your terminal and run:

`python -m pip install --proxy=http://localhost:3128 tqdm `

`python -m pip install --proxy=http://localhost:3128 Ruamel.yaml `

`python -m pip install --proxy=http://localhost:3128 requests3 `

`python -m pip install --proxy=http://localhost:3128 beautifulsoup4 `

`python -m pip install --proxy=http://localhost:3128 selenium `

## How to run the Change-Auditor (source code)

1. Open the repo on your terminal and run:
   `python main.py`

Note: You may have to lower your bit9 settings to run resources/chromedriver.exe

## How to run the Change-Auditor (executable release)

1. Download and extract or clone the branch 'feature/change-auditor-executable'
2. Contact TSC and request to have the file 'main.exe', located in the excutables folder of the above branch, whitelisted. \*have the exact filepath for this file ready when calling TSC
3. Once it has been whitelisted, the file can be run at anytime without specifically having your bit9 lowered

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
