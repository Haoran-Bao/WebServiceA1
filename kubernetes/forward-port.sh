#!/bin/sh

kubectl -n projectcontour port-forward service/envoy 8080:80 --address 0.0.0.0
