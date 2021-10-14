#!/bin/sh -l

echo "Hello $1, $2" # Usa o who-to-greed para printar "Hello [who-to-greed]"
time=$(date)
echo "::set-output name=time::$time"