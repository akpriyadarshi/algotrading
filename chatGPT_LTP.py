import requests

# Set the base URL for the API endpoint
base_url = 'https://smartapi.angelbroking.com/'

# Set the API endpoint for getting the LTP for Bank Nifty
endpoint = 'market/ltp/nifty_bank'

# Set the API key for your Angel Broking account
api_key = 'DmUofr3t'

# Set the headers for the API request
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Send the API request to get the LTP for Bank Nifty
response = requests.get(f'{base_url}{endpoint}', headers=headers)

# Check the status code of the response to ensure that it was successful
if response.status_code == 200:
    # The request was successful, so parse the response data
    data = response.json()
    ltp = data['ltp']
    print(f'The LTP for Bank Nifty is {ltp}.')
else:
    # The request was not successful, so print an error message
    print(f'An error occurred: {response.text}')

