# Remove old generated data
cd $TRAVIS_BUILD_DIR
rm ./_symbols/*.md
rm ./_footprints/*.md
rm ./_packages3d/*.md
rm ./download/*

# Run generator scripts
cd ./_scripts
python gen_symbol_info.py /home/travis/build/kicad-library/library/*.lib --schlib /home/travis/build/utils/schlib --output $TRAVIS_BUILD_DIR/_symbols --download $TRAVIS_BUILD_DIR/download/ --csv $TRAVIS_BUILD_DIR/_data/symbols.csv -v

# And back to the build dir
cd $TRAVIS_BUILD_DIR