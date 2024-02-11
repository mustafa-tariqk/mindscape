# This script must be run in the server directory.
mkdir -p docs
rm -rf docs/*
find . -name '*.py' -not -path "./venv/*" -exec python3 -m pydoc -w {} \;
mv *.html docs
