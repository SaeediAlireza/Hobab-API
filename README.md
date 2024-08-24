# Hobab-API

Hobab is an App for automation of fish farming specified for caviar fishes

## setting up

for installing requirments first set up mysql with no passwod for root user;
and use this command to install python requrements:

`pip install -r requrements.txt`

for running the server:
`fastapi dev main.py`
or
`uvicorn main:app`

and open this link for visiting documents:

[http://127.0.0.1:8000/docs]

# for https

first do this command to get keys:
`openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`

and for running the server use this command:
`uvicorn main:app --ssl-keyfile ./key.pem --ssl-certfile  ./cert.pem`
