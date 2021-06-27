import yaml
from box import Box
import requests
import json
import time
import telegram

def build_immo_url_from_config(cfg):
  """Builds immobilienscout url using config values to set request parameters"""

  with_balcony =  "-mit-balkon" if hasattr(cfg, 'with_balcony') and cfg.with_balcony else ""
  url = f"{cfg.url}{cfg.city}/{cfg.city}/wohnung{with_balcony}-mieten?"

  #Build parameters
  url += f"haspromotion={cfg.wbs}&"  if hasattr(cfg, 'wbs') and cfg.wbs is not None else ""
  url += f"numberofrooms={cfg.num_of_rooms}&" if hasattr(cfg, 'wbs') and cfg.num_of_rooms is not None else ""
  price_from =  cfg.price_from if (hasattr(cfg, 'price_from') and cfg.price_from is not None) else ""
  price_up_to = cfg.price_up_to if (hasattr(cfg, 'price_up_to') and cfg.price_up_to is not None) else ""
  url += f"price={price_from}-{price_up_to}&"  
  url += f"livingspace={cfg.livingspace}&" if  hasattr(cfg, 'livingspace') and cfg.livingspace  else ""
  url += f"price_type={cfg.price_type}&" if hasattr(cfg, 'price_type') and cfg.price_type  else ""
  url += f"floor={cfg.floor_from}" if hasattr(cfg, 'floor_from') and cfg.floor_from  else ""
  url += "&sorting=2"
  return url

def get_result_list(url):
  """Returns the available listings as an array of raw results"""
  r = requests.post(url)
  content = json.loads(r.content)
  result_list = content["searchResponseModel"]["resultlist.resultlist"]["resultlistEntries"][0]["resultlistEntry"]
  return result_list

def parse_result(result):
  """Parses the relevant info from the result json to a string for Telegram message"""
  res = result['resultlist.realEstate']['address']['quarter'] +'\n'
  res += "Total Rent: " + str(result['resultlist.realEstate']["calculatedTotalRent"]["totalRent"]["value"]) +'Eur\n'
  attributes = result['attributes'][0]['attribute']
  for a in attributes:
    res += str(a['label']) + ": " + str(a['value']) +'\n'
  res += "https://www.immobilienscout24.de/expose/" + result['@id']
  return res


def get_message_suggestion(result,cfg):
  """Prepares a message suggestions to send"""
  contact = result['resultlist.realEstate']['contactDetails']
  salutation = "Sehr geehrte"
  if 'lastname' in contact:
    salutation +=  " Frau " if contact['salutation'] == "FEMALE" else "r Herr "
    salutation += contact['lastname']
  else:
    salutation += " Damen und Herren"
  address = result['resultlist.realEstate']['address']['description']['text']
  text = f"{salutation},\n{cfg.text_before_address} {address} {cfg.text_after_address}" 
  print(text)
  return text

def log_result(result):
  """Logs the relevant info from the result"""
  print("id: "+result['@id'])
  print("title")
  print(result['resultlist.realEstate']['title'])
  print("address")
  print(result['resultlist.realEstate']['address'])
  print("contact")
  print(result['resultlist.realEstate']['contactDetails'])

  # print(json.dumps(result, sort_keys=False, indent=4))

def main():
  with open("config.yaml", "r",  encoding='utf-8') as ymlfile:
    cfg = Box(yaml.safe_load(ymlfile))

  # Don't get notified for the existing offers
  first_run = True
  m = set()
  url = build_immo_url_from_config(cfg.immoscout)
  bot = telegram.Bot(token=cfg.telegram.token)
  bot.sendMessage(chat_id = cfg.telegram.chat_id, text = "Start")
  while True:
    result_list = get_result_list(url)
    for result in result_list:
      if result['@id'] not in m:
        if not first_run:
          res = parse_result(result) 
          bot.sendMessage(chat_id = cfg.telegram.chat_id, text = res )        
          log_result(result)
          message_suggestion = get_message_suggestion(result,cfg.message)
          bot.sendMessage(chat_id = cfg.telegram.chat_id, text = message_suggestion )  
        m.add(result['@id'])
    first_run = False
    time.sleep(60)

if __name__ == '__main__':
  main()