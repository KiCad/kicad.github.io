# Generate footprint listings

rm _footprints/*.md
python gen_footprint_info.py /home/travis/build/footprints/*.pretty --script /home/travis/build/kicad-library -v --download download/ --output _footprints
