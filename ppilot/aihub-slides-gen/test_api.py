import requests

# API endpoint URL
api_url = "http://10.239.80.70:10000/convert"

# File names for testing
output_name = "example1"
input_name = "example1"

# Prepare data as form parameters
data = {"output_name": output_name, "input_name": input_name}

try:
    # Send POST request to API
    response = requests.post(api_url, data=data)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        print(f"PDF conversion successful. Downloaded file as {output_name}.pptx")
        # Save the downloaded file
        with open(f"{output_name}.pptx", "wb") as f:
            f.write(response.content)
    else:
        print(f"Error: {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Error sending request: {e}")
