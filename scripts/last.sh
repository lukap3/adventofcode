days=()
for entry in days/day*.py
do
  dayNum="${entry//[^0-9]/}"
  days+=("$dayNum")
done
if [ -n "${days[0]}" ]; then
  max=${days[0]}
  for n in "${days[@]}" ; do
      ((n > max)) && max=$n
  done

  python days/day$max.py
else
  echo "No day file found. Exiting"
  exit 1
fi
