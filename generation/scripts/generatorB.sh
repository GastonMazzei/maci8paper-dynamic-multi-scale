#!/bin/sh

echo "About to generate data..."

python3 scripts/generators/generatorB-1.py &
python3 scripts/generators/generatorB-2.py &
python3 scripts/generators/generatorB-3.py &
python3 scripts/generators/generatorB-4.py &

wait
echo "...Generation is complete"
