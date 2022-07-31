# APIGateway Service
The APIGateway has the following tasks:

1. Authentication:
    
   Authenticate users based on Authorization header with the following format '{walletAddress}:{expireTimestamp} {signature}'

2. Authorization:

    Define user role and access Based on authenticated wallet address.

3. Routing requests:

    This gateway routes requests to other micro services given in env variables.


## Authorization Token
Since the authentication and authorization are based on user wallet address there is no stored credentials or secret keys.

User should have a wallet (private key and public key pair). Then follow the following steps:

1. Make walleAddress which is lower case string of user wallet address (public key).

2. Create expireTimestamp which is current time stamp plus 4 hours (4 * 60 * 60 * 1000 ms) boths in mili seconds.

3. Create a message to sign:

    message := '{walletAddress}:{expireTimestamp}'

4. Create signature:

    signature := Sign the message with your wallet private key.
    
5. Create token:

    token := '{walletAddress}:{expireTimestamp} {signature}'

6. Put it in the request header:

    Authorization: token

Example:

To see the example of token creation see the get_token function in app/auth.py, you can also run the app/auth.py to generate a token.



# Execution

In the project directory you have the following options:

* Python:
    
    1. Install the requirments.txt file:

        ```
        pip install -r requirements.txt
        ```

    2.  Run it with uvicorn:

        ```
        uvicorn app.main:app
        ```

* Docker:

    Run the following command:
    ```
    docker-compose up
    ```
    or 
    ```
    docker-compose up -d 
    ```
    to run in detach mode.