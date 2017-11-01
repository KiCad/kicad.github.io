# Generate symbol listings
python gen_symbol_info.py /home/travis/build/kicad-library/library/*.lib --schlib /home/travis/build/kicad-library/schlib --output ../_symbols --json ../files/symbols.json -v --download ../download/ --csv ../_data/symbols.csv
gzip ../files/symbols.json -f