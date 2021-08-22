import requests
import json


class ImmoScout:
  def __init__(self, config):
    self.config = config
    self.url = self._build_immo_url_from_config()
    self.map = set()
    self.first_run = True

  def _build_immo_url_from_config(self):
    """Builds immobilienscout url using config values to set request parameters"""
    config = self.config
    if hasattr(config, 'whole_url') and config.whole_url:
      return config.whole_url
    with_balcony =  "-mit-balkon" if hasattr(config, 'with_balcony') and config.with_balcony else ""
    url = f"{config.url}{config.city}/{config.city}/wohnung{with_balcony}-mieten?"

    #Build parameters
    url += f"haspromotion={config.wbs}&"  if hasattr(config, 'wbs') and config.wbs is not None else ""
    url += f"shape={config.shape}&"  if hasattr(config, 'shape') and config.shape is not None else ""
    url += f"numberofrooms={config.num_of_rooms}&" if hasattr(config, 'wbs') and config.num_of_rooms is not None else ""
    price_from =  config.price_from if (hasattr(config, 'price_from') and config.price_from is not None) else ""
    price_up_to = config.price_up_to if (hasattr(config, 'price_up_to') and config.price_up_to is not None) else ""
    url += f"price={price_from}-{price_up_to}&"  
    url += f"livingspace={config.livingspace}&" if  hasattr(config, 'livingspace') and config.livingspace  else ""
    url += f"price_type={config.price_type}&" if hasattr(config, 'price_type') and config.price_type  else ""
    url += f"floor={config.floor_from}" if hasattr(config, 'floor_from') and config.floor_from  else ""
    url += "&sorting=2"
    return url

  def _get_raw_result_list(self):
    """Returns the available listings as an array of raw results"""
    response = requests.post(self.url)
    immoscout_ads_content = json.loads(response.content)
    raw_result_list = immoscout_ads_content["searchResponseModel"]["resultlist.resultlist"]["resultlistEntries"][0]["resultlistEntry"]
    return raw_result_list

  @staticmethod
  def parse_result(result):
    """Parses the relevant info from the result json to a string for Telegram message"""
    parsed_result = result['resultlist.realEstate']['address']['quarter'] +'\n'
    parsed_result += "Total Rent: " + str(result['resultlist.realEstate']["calculatedTotalRent"]["totalRent"]["value"]) +'Eur\n'
    attributes = result['attributes'][0]['attribute']
    for attribute in attributes:
      parsed_result += str(attribute['label']) + ": " + str(attribute['value']) +'\n'
    parsed_result += "https://www.immobilienscout24.de/expose/" + result['@id']
    return parsed_result


  def get_message_suggestion(self,result):
    """Prepares a message suggestions to send"""
    message_config =self.config.message
    contact = result['resultlist.realEstate']['contactDetails']
    salutation = "Sehr geehrte"
    if 'lastname' in contact:
      salutation +=  " Frau " if contact['salutation'] == "FEMALE" else "r Herr "
      salutation += contact['lastname']
    else:
      salutation += " Damen und Herren"
    address = result['resultlist.realEstate']['address']['description']['text']
    message_text = f"{salutation},\n{message_config.text_before_address} {address} {message_config.text_after_address}" 
    print(message_text)
    return message_text

  @staticmethod
  def log_result(result):
    """Logs the relevant info from the result"""
    print("id: "+result['@id'])
    print("title")
    print(result['resultlist.realEstate']['title'])
    print("address")
    print(result['resultlist.realEstate']['address'])
    print("contact")
    print(result['resultlist.realEstate']['contactDetails'])


  def get_new_ads_results(self):
    """Gets new ads starting from the second run, ignores the already existing ads """
    results = []
    raw_result_list = self._get_raw_result_list()
    for result in raw_result_list:
      if result['@id'] not in self.map:
        if not self.first_run:
          results.append(result)
        self.map.add(result['@id'])
    self.first_run = False
    return results

