#!/bin/bash

mc config host add storage http://minio:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

mc mb --ignore-existing storage/sources

mc anonymous set download storage/sources
