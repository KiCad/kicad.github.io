# Generate footprint listings

rm $TRAVIS_BUILD_DIR/_footprints/*.md
python gen_footprint_info.py $TRAVIS_BUILD_DIR/footprints/*.pretty --script $TRAVIS_BUILD_DIR/kicad-library-utils -v --download $TRAVIS_BUILD_DIR/download/ --output $TRAVIS_BUILD_DIR/_footprints
