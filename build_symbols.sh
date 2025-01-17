# Pull requests and commits to other branches shouldn't try to deploy, just build to verify
if [ "$TRAVIS_PULL_REQUEST" != "false" -o "$TRAVIS_BRANCH" != "master" ]; then
    echo "Skipping deploy; just doing a build."
    exit 0
fi

# Remove old generated data
cd $TRAVIS_BUILD_DIR

rm _symbols/*.md
rm _symbols/*.html

# copy over symbol library table to downloads directory
cp /home/travis/build/kicad-symbols/sym-lib-table $TRAVIS_BUILD_DIR/download/symbols/.

# Generate symbol data
python _scripts/gen_symbol_info.py /home/travis/build/kicad-symbols/*.lib --schlib /home/travis/build/utils/schlib --output $TRAVIS_BUILD_DIR/_symbols --download $TRAVIS_BUILD_DIR/download/ -v
