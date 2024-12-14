#!/bin/bash

mkdir certs
openssl genrsa -out certs/jwt-private.pem 2048 \
&& openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem