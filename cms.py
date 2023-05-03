import requests
import requests.packages.urllib3.util.connection as urllib3_cn
import socket

CMS_URL_BASE = "http://localhost:1337"
CMS_URL_WEBSITE_CONTENT = f"{CMS_URL_BASE}/api/website-content?populate=*"



def send_cms_request() -> dict:
    urllib3_cn.allowed_gai_family = lambda: socket.AF_INET
    cms_response_data = requests.get(CMS_URL_WEBSITE_CONTENT).json()
    return cms_response_data

def parse_cms_response(cms_response: dict) -> dict:
    parsed_cms_data = {}

    for key, value in cms_response["data"]["attributes"].items():
        if type(value) != dict:
            parsed_cms_data[key] = value
            continue

        parsed_cms_data[key] = value["data"]["attributes"]["url"]

    return parsed_cms_data

def get_cms_content() -> dict:
    cms_response = send_cms_request()
    parsed_cms_data = parse_cms_response(cms_response)
    
    return parsed_cms_data

def format_cms_image(img_endpoint):
    return f"{CMS_URL_BASE}{img_endpoint}"