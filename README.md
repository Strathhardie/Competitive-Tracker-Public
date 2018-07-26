# change-checker

A Web Scraper application to automate the compilation of interest rate data from various competitor websites. This repository specifically detects if the HTML of a website has changed since the last run.

## How to clone & connect to this repository

1. On Git Bash, configure the Proxy settings by entering this command. The port may be different depending on CNTLM settings:
`` git config --global http.proxy "127.0.0.1:5128" `` 

2. Create a personal access token by following this guide: https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/

The SSH port 22 seems to be blocked by the firewall, so clone using HTTPS.

## How to install the dependencies

1. After cloning this repository, open it on your terminal and run:

`` pip install resources/selenium-3.13.0-py2.py3-none-any.whl ``

## How to run the change-checker

1. Open the repo on your terminal and run:
`` python demo.py ``