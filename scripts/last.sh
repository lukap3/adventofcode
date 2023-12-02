directory="$YEAR/days"

day_numbers=$(find "$directory" -type f -name "day*.py" -exec basename {} \; | grep -o -E '[0-9]+' | sort -n)

max_day=$(echo "$day_numbers" | tail -n 1)

python $directory/day$max_day.py
