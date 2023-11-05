# SampleTelegramQuiz
Sample of Telegram Quiz in Python

Find here the source code of the [Creating a Telegram Chatbot Quiz with Python](https://towardsdatascience.com/creating-a-telegram-chatbot-quiz-with-python-711a43c0c424) 
article.

![Alt text](splash.png?raw=true "World Capitals Quiz")

### Table of Contents 
  * [Setup](#setup)
  * [Run on Local](#run-on-local)
  * [Run on AWS EC2 instance](#run-on-aws-ec2-instance)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## Setup

Clone the repository

```
git clone https://github.com/lydnguyen/StudyBuddy.git
```

Create and *.env* file in the same folder as *StudyBuddy*. 
Install the packages in requirement.txt
```
pip install -r requirements.txt
```
The *.env* file defines the environment variables. To set environment variable via windows commandline:
```
set TELEGRAM_TOKEN={your Telegram token}
```

## Run on Local
Run the application
```
cd telegram_bot
python studybuddyapp.py
```
Access the bot via the deeplink `https://t.me/{bot_username}` and start chatting

**Note**: the chatbot runs in Polling mode

## run-on-aws-ec2-instance
https://abhinand05.medium.com/run-any-executable-as-systemd-service-in-linux-21298674f66f
https://snehalchaure.medium.com/running-an-application-as-a-service-with-systemctl-63a51dece4c5