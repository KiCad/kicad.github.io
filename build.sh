# Pull requests and commits to other branches shouldn't try to deploy, just build to verify
if [ "$TRAVIS_PULL_REQUEST" != "false" -o "$TRAVIS_BRANCH" != "master" ]; then
    echo "Skipping deploy; just doing a build."
    exit 0
fi

# Remove old generated data
cd $TRAVIS_BUILD_DIR

git checkout master

rm ./_symbols/*.md
rm ./_footprints/*.md
rm ./_packages3d/*.md

# Run generator scripts
cd ./_scripts

# Generate symbol data
python gen_symbol_info.py /home/travis/build/kicad-library/library/*.lib --schlib /home/travis/build/utils/schlib --output $TRAVIS_BUILD_DIR/_symbols --download $TRAVIS_BUILD_DIR/download/ --csv $TRAVIS_BUILD_DIR/_data/symbols.csv -v

# Generate footprint data
python gen_footprint_info.py /home/travis/build/footprints/*.pretty --script /home/travis/build/utils -v --download $TRAVIS_BUILD_DIR/download --output $TRAVIS_BUILD_DIR/_footprints

# Generate 3D model data
python gen_3dmodel_info.py /home/travis/build/kicad-library/modules/packages3d/*.3dshapes --output $TRAVIS_BUILD_DIR/_packages3d --download $TRAVIS_BUILD_DIR/download -v

# Generate library description information
python make_descriptions.py --table /home/travis/build/kicad-library/template/sym-lib-table --csv $TRAVIS_BUILD_DIR/_data/symbols.csv
python make_descriptions.py --table /home/travis/build/footprints/fp-lib-table --csv $TRAVIS_BUILD_DIR/_data/footprints.csv

# And back to the build dir
cd $TRAVIS_BUILD_DIR
