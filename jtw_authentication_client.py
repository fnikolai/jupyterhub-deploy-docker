import jwt
import requests
import datetime

# Secret key used for encoding the JWT
SECRET_KEY = '<secret-key>'

# Function to create a JWT
def create_jwt():
    # Define the payload
    payload = {
        'username': 'skata',
        'iss': 'your-issuer',             # Issuer
        'sub': 'your-subject',            # Subject
        'iat': datetime.datetime.utcnow(),  # Issued at
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expiration time
    }

    # Encode the JWT with the secret key
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Function to send the JWT to the server
def send_jwt(token):
    url = 'http://localhost:8000'
    headers = {
 #       'Authorization': f'Bearer {token}'
         'X-Auth-Token': token
    }

    # Send a GET request with the JWT in the Authorization header
    response = requests.get(url, headers=headers)

    # Print the response from the server
    print('Status Code:', response.status_code)
    print('Response Body:', response.text)

# Main function
if __name__ == '__main__':
    token = create_jwt()
    send_jwt(token)

