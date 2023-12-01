for entry in ./days$YEAR/day*.py
do
  # Check if the entry is an existing file
  if [ -e "$entry" ]; then
    echo ""
    echo "----- Running $entry -----"
    python "$entry"
  fi
done
