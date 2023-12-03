days=()
directory="$YEAR/days"

day_numbers=$(find "$directory" -type f -name "day*.py" -exec basename {} \; | grep -o -E '[0-9]+' | sort -n)

max_day=$(echo "$day_numbers" | tail -n 1)
max_day=$((10#$max_day))
next=$((max_day+1))
next=$(printf "%02d" $next)

echo "Generating day $next"

mkdir -p $YEAR
mkdir -p $YEAR/data
mkdir -p $YEAR/days
mkdir $YEAR/data/day$next
touch $YEAR/data/day$next/data.txt
touch $YEAR/data/day$next/example.txt
cp template $YEAR/days/day$next.py
sed -i '' "s/dayX/$YEAR\/data\/day$next/" $YEAR/days/day$next.py

if python fetch.py ${YEAR} $next; then
  echo "Files generated"
else
  rm -r $YEAR/data/day$next
  rm $YEAR/days/day$next.py
  exit 1
fi
