days=()
directory="days$YEAR"

day_numbers=$(find "$directory" -type f -name "day*.py" -exec basename {} \; | grep -o -E '[0-9]+' | sort -n)

max_day=$(echo "$day_numbers" | tail -n 1)
next=$((max_day+1))

echo "Generating day $next"

mkdir -p data$YEAR
mkdir data$YEAR/day$next
touch data$YEAR/day$next/data.txt
touch data$YEAR/day$next/example.txt
cp template days$YEAR/day$next.py
sed -i '' "s/dayX/day$next/" days$YEAR/day$next.py

if python fetch.py ${YEAR} $next; then
  echo "Files generated"
else
  rm -r data$YEAR/day$next
  rm days$YEAR/day$next.py
  exit 1
fi
