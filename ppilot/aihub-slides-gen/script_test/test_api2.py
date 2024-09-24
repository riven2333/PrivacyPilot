import requests
import os
os.environ["NO_PROXY"] = "127.0.0.1"

# API endpoint URL
api_url = 'http://10.239.80.70:10000/docs'



# Prepare data as form parameters
data = {
    "cmd": "time"
}

try:
    # Send POST request to API
    response = requests.post(api_url, data=data)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        print(f'Receive: {response.msg}.pptx')
    else:
        print(f'Error: {response.status_code} - {response.text}')

except requests.exceptions.RequestException as e:
    print(f'Error sending request: {e}')
