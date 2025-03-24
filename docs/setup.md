# Setup

## Prerequisites

This project provides a Dockerfile and a Docker Compose configuration file that can be used to run the project locally with Docker Compose and Docker Desktop.

- [Docker Compose](https://docs.docker.com/compose/)
- [Docker Desktop](https://docs.docker.com/desktop/)

This project is designed to display data from the JMDict_e database file from the JMdict project. The latest version of the file can be downloaded from [the JMDict Project Site](https://www.edrdg.org/jmdict/j_jmdict.html) by selecting *the current version with only the English translations*.

## Configuration

Copy the contents of `conf/env.example` to `.env` in the root of the project directory and fill in the configuration as instructed by the code comments in the file.

## Build the container images

To build the container images, run `docker compose build`.

## Start the application

To start the application, run `docker compose up`.

It takes a few minutes for the `scripts/init_dictionary.py` script to initialize the database with the data from the dictionary file. Once it is complete, the application can be accessed from http://localhost:8000.
