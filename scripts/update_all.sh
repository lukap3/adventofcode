directory="$YEAR/days"

day_numbers=$(find "$directory" -type f -name "day*.py" -exec basename {} \; | grep -o -E '[0-9]+' | sort -n)

for day_number in $day_numbers; do
    python fetch.py ${YEAR} $day_number
done
