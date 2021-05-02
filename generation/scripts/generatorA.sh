#!/bin/sh

echo "About to generate data..."

python3 scripts/generators/generatorA-1.py &
python3 scripts/generators/generatorA-2.py &
python3 scripts/generators/generatorA-3.py &
python3 scripts/generators/generatorA-4.py &

wait
echo "...Generation is complete"
