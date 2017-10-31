# Generate symbol listings
python gen_symbol_info.py ~/kicad/share/kicad-library/library/*.lib --schlib ~/kicad/utils/schlib --output ../_symbols --json ../files/symbols.json -v --download ../download/ --csv ../_data/symbols.csv
gzip ../files/symbols.json -f