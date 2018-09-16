#!/bin/bash

curl https://data.baltimorecity.gov/api/views/zqh4-9ud5/rows.csv?accessType=DOWNLOAD | cut -d, -f3 | grep http | cut -d\& -f1 | xargs -I{} curl -LO {}
