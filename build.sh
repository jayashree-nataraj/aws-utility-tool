#!/usr/bin/env bash

echo
docker build -t aws-utility-tool --build-arg "$1" --build-arg "$2" .
if [ $? -gt 0 ]; then
  echo
  echo "Docker build FAILED, aborting!"
  echo
  exit 1
fi
