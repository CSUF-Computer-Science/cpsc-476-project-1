# Docker Image

## Intro

For those among us who run Linux and don't want to virtualize Tuffix or install the nginx package globally.

The Dockerfile provided here will generate an nginx Docker image for our nginx load balancer testing.

## Usage

1) `docker build -t blog .`
2) Start the Foreman formation
3) `docker run --network host -it blog`

Nginx will then be running with the `blog` config and will foreward requests to the blog microservices.

Press `Ctrl+C` from the `docker run ...` prompt to stop the nginx server.
