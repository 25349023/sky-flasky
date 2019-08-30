#!/bin/sh

while true; do
    pipenv run flask deploy
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed: $?, retrying in 5 secs...
    sleep 5
done

exec pipenv run gunicorn -b :5000 --access-logfile - --error-logfile - flasky:app

