# Generate footprint listings

rm ../_footprints/*.md
python gen_footprint_info.py ~/kicad/share/pretty/*.pretty --script ~/kicad/utils -v --download ../download/ --output ../_footprints
