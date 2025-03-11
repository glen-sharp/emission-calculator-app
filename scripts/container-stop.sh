#!/usr/bin/env bash

set -e

docker stop emission-frontend && docker rm emission-frontend

docker stop emission-api && docker rm emission-api