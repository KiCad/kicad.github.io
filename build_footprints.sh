# Pull requests and commits to other branches shouldn't try to deploy, just build to verify
if [ "$TRAVIS_PULL_REQUEST" != "false" -o "$TRAVIS_BRANCH" != "master" ]; then
    echo "Skipping deploy; just doing a build."
    exit 0
fi

# Remove old generated data
cd $TRAVIS_BUILD_DIR

rm _footprints/*.md
rm _footprints/*.html

# copy over footprint library table to downloads directory
cp /home/travis/build/footprints/fp-lib-table $TRAVIS_BUILD_DIR/download/footprints/.

# Generate footprint data
python _scripts/gen_footprint_info.py /home/travis/build/footprints/*.pretty --script /home/travis/build/utils -v --download $TRAVIS_BUILD_DIR/download --output $TRAVIS_BUILD_DIR/_footprints
