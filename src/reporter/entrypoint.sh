reporter run age -e "2019-08-15T12:00:00+00:00" -o 480 \
 && reporter run status -e "2019-12-27T11:00:00+00:00" -o 360 \
 && reporter run estimate -e "2019-10-01T12:00:00+00:00" -o 240 \
 && reporter schedule status -s "*/5 * * * *" -o 5 \
 && reporter schedule age -s "*/5 * * * *" -o 5 \
 && reporter schedule estimate -s "*/5 * * * *" -o 5 \
 && cron -f