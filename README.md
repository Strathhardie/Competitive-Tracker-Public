# change-checker

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

## How to run the change-checker (source code)

1. Open the repo on your terminal and run:
`` python main.py ``

Note: You may have to lower your bit9 settings to run resources/chromedriver.exe

## How to run the change-checker (executable release)

1. Unzip [releases/change_checker_0.0.1.zip](releases/change_checker_0.0.1.zip)
2. Run main/main.exe

Note: You may have to lower your bit9 settings to run main.exe