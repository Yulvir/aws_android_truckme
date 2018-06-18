import json
import requests
import base64

def test_api_dau():

    #url = f'https://0y12gfrfo0.execute-api.eu-west-1.amazonaws.com/labcave/prod/DAU?{start_date_str}&{bundle_id_str}&{os_str}'
    url = f'https://bcqwuhc39f.execute-api.us-east-2.amazonaws.com/testing/jojo'

    key = "Qbu0MkRw4a78sS1HF9k5xaO7M278Kzuq6egbgIaD"
    auth_header = {'content-type': 'application/json', "Content-Encoding": "gzip", 'x-api-key': key}
    response = requests.get(url, headers=auth_header)
    print(response)
    print(json.loads(base64.b64decode(response.content)))


if __name__ == '__main__':

    test_api_dau()
