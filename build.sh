# Remove old generated data
cd $TRAVIS_BUILD_DIR
rm ./_symbols/*.md
rm ./_footprints/*.md
rm ./_packages3d/*.md

# Run generator scripts
cd ./_scripts
echo "what is here?"
ls .
echo "What is there?"
ls /home/travis/build/kicad-library/
echo "What is in libs?"
ls /home/travis/build/kicad-library/library/
python gen_symbol_info.py /home/travis/kicad-library/library/*.lib --schlib /home/travis/build/utils/schlib --output $TRAVIS_BUILD_DIR/_symbols --download $TRAVIS_BUILD_DIR/download/ --csv $TRAVIS_BUILD_DIR/_data/symbols.csv -v

echo "Ok, script is done now"