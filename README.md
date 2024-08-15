# Hobab-API

Hobab is an App for automation of fish farming specified for caviar fishes

# for https

first do this command to get keys:
`openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`

and for running the server use this command:
`uvicorn main:app --ssl-keyfile ./key.pem --ssl-certfile  ./cert.pem`
