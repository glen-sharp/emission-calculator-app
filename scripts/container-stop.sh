#!/usr/bin/env bash

set -e

if [ $# -eq 0 ]; then
  echo "Error: No parameter provided"
  exit 1
fi

CONTAINER_APP=$1

$CONTAINER_APP stop emission-frontend && $CONTAINER_APP rm emission-frontend

$CONTAINER_APP stop emission-api && $CONTAINER_APP rm emission-api