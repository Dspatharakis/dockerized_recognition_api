#!/usr/bin/env bash
kubectl delete hpa edge-server-cv
kubectl delete svc edge-server-cv
kubectl delete deployment edge-server-cv
kubectl apply -f edge-server-service.yaml 
kubectl apply -f edge-server-deployment-big.yaml 
kubectl apply -f edge-server-hpa-custom-big.yaml 

