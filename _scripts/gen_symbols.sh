# Generate symbol listings
rm $TRAVIS_BUILD_DIR/_symbols/*.md
python gen_symbol_info.py $TRAVIS_BUILD_DIR/kicad-library/library/*.lib --schlib $TRAVIS_BUILD_DIR/kicad-library/schlib --output $TRAVIS_BUILD_DIR/_symbols --json $TRAVIS_BUILD_DIR/files/symbols.json -v --download $TRAVIS_BUILD_DIR/download/ --csv $TRAVIS_BUILD_DIR/_data/symbols.csv
gzip $TRAVIS_BUILD_DIR/files/symbols.json -f