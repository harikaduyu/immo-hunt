<img src="https://img.shields.io/github/license/harikaduyu/immo-hunt">
<img src="https://img.shields.io/maintenance/yes/2021">
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg"></a>

# immo-hunt

A telegram bot app, which sends new offers from immobilienscout website based on some filters as a telegram message. It also sends a recommended message to send to the poster of the offer, using offer address and contact details.

It is inspired by [immo-trakt](https://github.com/mustafabayar/immo_trakt) but this one is written in python and also sends a suggested message text tailor made for the offer.

## How to use it? 

### Setting up config
Copy `config_example.yaml` file and/or rename it `config.yaml`. In this config file there are three sections:
- `immoscout`

Has your filters for looking for a flat. You can also directly copy the [url](https://www.immobilienscout24.de/Suche/shape/wohnung-mieten?shape=fWltX0ltbHZwQXhoQHdtSW9nQnd2QHFoQXZoQnxWcGNEO2V8cV9JeXp_cEF_SGtNd0N5X0A.&numberofrooms=3.0-&livingspace=70.0-&enteredFrom=result_list&viewMode=MAP#/?boundingBox=52.130122%2C11.886509%2C52.88074%2C14.962681) which gives the list of flats based your filters and paste it to `whole_url` section. Then all others will be ignored. This is useful when there is a drawing for the location filter.
- `telegram`

You need two values to connect your app to a telegram bot which sends messages to a chat. 
First you need to create a telegram bot using [The BotFather](https://telegram.me/BotFather). Follow the instructions to get the `token` for your bot.

You can obtain the `chat_id` by using this API -> https://api.telegram.org/bot\<YourBOTToken\>/getUpdates

Add your bot `token` in the url. Ex:
```
 https://api.telegram.org/bot123456789:jbd78sadvbdy63d37gda37bd8/getUpdates
```
Look for the "chat" object:
```json
{"ok":true,"result":[{"update_id":854999095,
"message":{"message_id":1264,"from":{"id":1234567890,"is_bot":false,"first_name":"Harika","language_code":"en"},"chat":{"id":<ChatIdYouAreLookingFor>,"first_name":"Harika","type":"private"},"date":1633171653,"text":"Hey"}}]}
```

❗ Make sure you've recently sent some messages to your bot, via your desired chat that you'd like to use later. 
- `message`

Whenever there is a new add, the bot will send the ad link along with a suggested message. This is the part where you define what the message will be. You can ignore the part with the salutation because app will parse the sender's data and decide whether it will be 
```
Sehr geehrter Herr XXX,
``` 
or 
```
Sehr geehrte Frau XXX,
```
 or
```
Sehr geehrte Damen und Herren,
```
The app will also parse the address of the flat and add it to the message, so separate your text into two parts where the address will go in between.
### Run locally with python/pipenv

Make sure you have python installed:

```
$  python -V
Python 3.8.2
```
and pip is available:
```
$  pip -V
pip 21.2.4 
```
Then instal pipenv:
```
pip install --user pipenv
```

Or install pipenv by following [these steps](https://pipenv.pypa.io/en/latest/install/). 
Then install dependencies:
```
pipenv install
```
And go into env shell with
```
pipenv shell
```
Now you are ready to run the app

```
python app.py
```
### Run locally with Docker
Coming soon..