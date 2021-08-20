# sqlGram
Telegram bot that provides a simple sql shell for any mysql DB

## Setup

### In the shell

Clone the repo (`git clone git@github.com:MatMasIt/sqlGram.git`)

Install the dependencies wth ` pip install -r requirements.txt` or `pip3 install -r requirements.txt`

Create a bot with [@BotFather](https://t.me/BotFather)

Fill in `conf.ini` with the mysql db details and the bot id

Run the bot (`python3 main.py`)

Copy the token

### In Telegram

Start the bot

Send the token

Once authed, send the commands.

Your account will be the only one to be able to use the bot.


## Usage Notes

Large responses are sent as a `results.txt` file

You may prepend `CSV` or `JSON` in front of a query to set the output format, default is a text table
