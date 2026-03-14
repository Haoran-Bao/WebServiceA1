#!/bin/sh

kubectl port-forward services/nginx 80:80 --address 0.0.0.0
