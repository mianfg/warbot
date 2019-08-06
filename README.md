<p align="center">
    <img src="./warbot/resources/logo.png" width="500px">
</p>

<h1 align="center"><p align="center">Bloomgogo War Bot</h1></h1>

> Created by **Miguel Ángel Fernández Gutiérrez** · https://mianfg.bloomgogo.com/

## Introduction

**Bloomgogo War Bot** is a Twitter and Telegram bot that makes it easy to create live battles between Twitter users; it consists of:

* A **Telegram bot** that serves as an _admin_, for an authorized user to control all the characteristics of the came.
* A **Twitter client** that automatically extracts information and posts tweets to Twitter, based on the settings specified by the client.

## The War

The war consists on battles between users, the last one to be alive is the winner!

First, we have to consider two types of "users":

* **Candidates:** Twitter users that are not yet "warriors" or "users", they can opt-in the candidates list. Then, the admin can promote them to **users**.
* **Users:** are the ones who fight in battles.

The admin can control the following features:

* **Battle scheduling:** there is a scheduling system to program battles based on battle frequencies, dates, etc.
* **Opt-in:** Twitter users can automatically enter to the candidates list if the opt-in option is enabled, by simply mentioning the bot's Twitter username in a tweet.
* **New user announce:** new users can be announced to the Twitter's bot account, either natively or for certain users.
* **Battle updates:** the app has a system to post tweets with images and lists to Twitter, to mantain the bot's user base updated about the war.

## Documentation

> Right now, a documentation site is being built on [Bloomgogo](https://bloomgogo.com/). For now, you can consult the documentation in the individual Python folders. Every method, class and variable is thoroughly documented.

## File structure

| Name | Description |
| --- | --- |
| [**bots**](./bots) | Contains two scripts, one for each bot |
| ├── [telegram_bot.py](./bots/telegram_bot.py) | Telegram bot |
| └── [twitter_bot.py](./bots/twitter_bot.py) | Twitter bot |
| [**database**](./database) | Contains database files |
| └── [warbot_db.json](./database/warbot_db.json) | TinyDB JSON database. _This can be modified in `vars.py`._ |
| [**lib**](./lib) | Contains app's classes and modules |
| ├── [admin.py](./lib/admin.py) | `WarBotAdmin` |
| ├── [api.py](./lib/api.py) | `WarBotAPI` |
| ├── [database.py](./lib/database.py) | `WarBotDB` |
| ├── [imagehandler.py](./lib/imagehandler.py) | `WarBotImageHandler` |
| ├── [telegram.py](./lib/telegram.py) | `TelegramInterface` |
| ├── [twitter.py](./lib/twitter.py) | `WarBotTwitter` |
| ├── [vars.py](./lib/vars.py) | Contains _environment_ variables |
| └── [warbot.py](./lib/warbot.py) | `WarBot` |
| [**logs**](./logs) | We recommend storing the logs here |
| [**resources**](./resources) | Contains resources for image generating, also this app's logo |
| [**tmp**](./tmp) | Folder where the images generated will be stored temporarily |

## Class structure

| Name | Description | File |
| --- | --- | --- |
| `TelegramInterface` | This module interacts directly with the Telegram API | [lib/telegram.py](./lib/telegram.py) |
| `WarBot` | Main controller for Bloomgogo War Bot | [lib/warbot.py](./lib/warbot.py) |
| `WarBotAdmin` | This module interacts with the Telegram bot | [lib/admin.py](./lib/admin.py) |
| `WarBotAPI` | This module interacts with the Twitter API | [lib/api.py](./lib/api.py) |
| `WarBotImageHandler` | This module generates images | [lib/imagehandler.py](./lib/imagehandler.py) |
| `WarBotDB` | This module controls the database, in TinyDB | [lib/database.py](./lib/database.py) |
| `WarBotTwitter` | This module interacts with `WarBotAPI` to deliver messages to Twitter | [lib/twitter.py](./lib/twitter.py) |

## How to set up the bot

The bot can be set up by executing the scripts `telegram_bot.py` and `twitter_bot.py` simultaneously. This functionality has been shortcut, and you can simply execute the `warbot` module:

```
python -m warbot
```

> To execute it, this way, you must be located on this repo's main folder, having the folder `warbot` listed by `ls` (to clarify).

Please refer to [requirements](#requirements) for more information on the libraries and versions that have been tested.

### Setting up variables

The `vars.py` file contains an amount of variables that control the bot. You can generate them by **making a Twitter app** and **starting a Telegram bot**.

* **Make a Twitter app.** You will need a Twitter Developers account. More information can be found on the [Twitter Developers](https://dev.twitter.com/) website.

    > **NOTE:** the only permissions needed are read and write, no direct message functionality is yet used in this bot.
* **Start a Telegram bot.** This can be easily done using Telegram's **Bot Father**. Start a conversation with `@botfather` on Telegram and simply go along!

### Some things for Bot Father

Telegram bots incorporate the useful functionality of shortcutting the commands by integrating them in the Telegram app's GUI. To do this, you have to talk to Bot Father using the command `/setcommands`, selecting your bot and then sending it the following message:

>help - Show help
>runoptin - Enable opt-in
>stopoptin - Disable opt-in
>nextbattle - Next battle info
>schedulebattle - Schedule next battle
>battlefrequency - Battle frequency
>setbattlefrequency - Set frequency
>stopfrequency - Ignore frequency
>forcebattle - Force battle
>getfighters - Get all fighters
>getfighter - Info about a fighter
>getcandidates - Get all candidates
>addfighter - Add fighter
>deletefighter - Delete fighter
>addcandidate - Add candidate
>deletecandidate - Delete candidate
>revive - Revive fighter
>announcefighters - Automatically announce fighters
>stopannouncefighters - Do not automatically announce fighters
>status - Bot status
>restart - Restart database

Of course, the information is scarce, but do not hesitate to use the `/help` command for more detailed info.

## Requirements

These are the libraries used under testing. You can create a virtual environment to use these versions. View `pip` and `virtualenv`'s documentation for more info.

```
tweepy==3.7.0
tinydb==3.13.0
requests==2.18.4
urllib3==1.22
numpy==1.16.4
Pillow==5.1.0
```

This project has been executed in **Python 3.6**.

## Credits

This project could not have been created without the help of the following libraries, and the communities that have created them and actively mantain them:

* [**Tweepy**](https://tweepy.org/), a library for communicating with Twitter's API.
* [**TinyDB**](), a minimal database.
* [**Pillow**](https://pillow.readthedocs.io/en/stable/), un fork de **PIL** (Python Image Library).

> Of course, I also highly credit and thank the authors and mantainers of the rest of the libraries used. However, I have thought appropiate to specially mention these as they are a core part of this app's programming.