import configparser
import requests
import time
from datetime import datetime

if __name__ == '__main__':
    # OPENING CONFIG FILE
    parser = configparser.ConfigParser()
    parser.read("settings.cfg")

    # READING API CONFIG
    key = parser.get("API", "api_key")
    host = parser.get("API", "api_server")
    cfg_param = parser.get("API", "cfg_param")

    # READING GENERAL CONFIG
    retry_delay = int(parser.get("CONFIG", "retry_delay"))
    max_retries = int(parser.get("CONFIG", "max_retries"))

    # PREPARING REQUESTS
    api_url = f"https://{host}/api/?{cfg_param}&key={key}"
    for x in range(max_retries):
        response = requests.get(api_url, verify=False)
        if (response.status_code >= 200 and  response.status_code < 300):
            content = response.content.decode("utf-8")

            # SAVE TO A FILE
            with open(f"BKP_PA_{datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}.xml", "w") as f:
                f.write(content)
            
            break
        time.sleep(retry_delay)