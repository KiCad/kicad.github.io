# Generate symbol listings
echo "Ok, here we go!"
ls /home/travis/build/kicad-library/library/
python gen_symbol_info.py /home/travis/build/kicad-library/library/*.lib --schlib /home/travis/build/utils/schlib --output $TRAVIS_BUILD_DIR/_symbols --json $TRAVIS_BUILD_DIR/files/symbols.json -v --download $TRAVIS_BUILD_DIR/download/ --csv $TRAVIS_BUILD_DIR/_data/symbols.csv
gzip $TRAVIS_BUILD_DIR/files/symbols.json -f