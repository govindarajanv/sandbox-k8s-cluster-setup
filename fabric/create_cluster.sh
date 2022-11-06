#!/bin/bash

echo "Configure the master..."
fab get-addresses --type=master create-cluster


echo "Configure the workers..."
fab get-addresses --type=workers configure-worker-node
sleep 20

echo "Running a sanity check..."
fab get-addresses --type=master get-nodes
