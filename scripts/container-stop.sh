#!/usr/bin/env bash

podman stop emission-frontend && podman rm emission-frontend

podman stop emission-api && podman rm emission-api