import yaml
from box import Box
import requests
import json



def build_immo_url_from_config(cfg):
  """Builds immobilienscout url using config values to set request parameters"""

  mit_balkon = cfg.mit_balkon if hasattr(cfg, 'mit_balkon') else ""

  url = f"{cfg.url}{cfg.city}/{cfg.city}/wohnung{mit_balkon}-mieten?"

  #Build parameters
  url += f"haspromotion={cfg.wbs}&"  if hasattr(cfg, 'wbs') and cfg.wbs is not None else ""

  url += f"numberofrooms={cfg.num_of_rooms}&" if hasattr(cfg, 'wbs') and cfg.num_of_rooms is not None else ""

  price_from =  cfg.price_from if (hasattr(cfg, 'price_from') and cfg.price_from is not None) else ""
  price_up_to = cfg.price_up_to if (hasattr(cfg, 'price_up_to') and cfg.price_up_to is not None) else ""
  url += f"price={price_from}-{price_up_to}&"  

  url += f"livingspace={cfg.livingspace}&" if  hasattr(cfg, 'livingspace') and cfg.livingspace  else ""

  url += f"price_type={cfg.price_type}&" if hasattr(cfg, 'price_type') and cfg.price_type  else ""

  url += f"floor={cfg.floor_from}" if hasattr(cfg, 'floor_from') and cfg.floor_from  else ""

  return url

def get_api_response():
  pass

# r = requests.post(url)
# content = json.loads(r.content)
# result_list = content["searchResponseModel"]["resultlist.resultlist"]["resultlistEntries"][0]["resultlistEntry"]
# print(len(result_list))
# for result in result_list:
#   print(result)


def main():
  with open("config.yaml", "r") as ymlfile:
    cfg = Box(yaml.safe_load(ymlfile))

  url = build_immo_url_from_config(cfg.immoscout)
  print(url)



if __name__ == '__main__':
  main()