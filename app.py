import yaml
from box import Box
import time
import telegram

from immoscout_agent import ImmoScout


def main():
  with open("config.yaml", "r",  encoding='utf-8') as ymlfile:
    config = Box(yaml.safe_load(ymlfile))

  # Don't get notified for the existing offers
  immoscout_agent = ImmoScout(config.immoscout)
  bot = telegram.Bot(token=config.telegram.token)
  bot.sendMessage(chat_id = config.telegram.chat_id, text = "Start")
  while True:
    for immo_result in immoscout_agent.get_new_ads_results():
      parsed_result = immoscout_agent.parse_result(immo_result) 
      bot.sendMessage(chat_id = config.telegram.chat_id, text = parsed_result )        
      immoscout_agent.log_result(immo_result)
      message_text = immoscout_agent.get_message_suggestion(immo_result)
      bot.sendMessage(chat_id = config.telegram.chat_id, text = message_text )  

    time.sleep(60)

if __name__ == '__main__':
  main()