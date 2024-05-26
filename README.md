# AI Powered Telegram Bot

This is a telegram bot powered by AI.

## How to run this?

You need docker installed for this.

### Build

```sh
docker build -t dana-bot:latest .
```

### Setup

Create a .env file somewhere on your disk.
edit the content of the .env file and add the following keys:

```
ALLOWED_USERS=user1,user2
BOT_TOKEN=11111111111:AAAAAAAAAAAAAAAAAAAAAAAA
OPENAI_API_KEY=???
OPEN_AI_MODEL_NAME=gpt-4-turbo
GOOGLE_CSE_ID=???
GOOGLE_API_KEY=???
OPENWEATHERMAP_API_KEY=???
```

`ALLOWED_USERS` is a comma separated list of users who can use this bot.
Add your telegram username or whoever you want to use this bot to this list.

For ``, you need to create the instructions here:
https://core.telegram.org/bots/features#botfather in order to create your own bot.
Then grab the token and stick it in here.

`OPENAI_API_KEY` is mandatory for this bot to run. You need to create an OpenAI accoutn for this.
In the future I'll add llama powered bot support as well.

The `GOOGLE_CSE_ID`, `GOOGLE_API_KEY`, and `OPENWEATHERMAP_API_KEY` keys are
optional. If you add them, the bot will be able to do google search or get
the weather report for various places.

### Run locally

Finally, when you have this file populated, you can easily run it using the following command:

```sh
docker run -t --rm -v $PWD:/etc/dana-bot --name data-bot dana-bot:latest
```
