# Pull requests and commits to other branches shouldn't try to deploy, just build to verify
if [ "$TRAVIS_PULL_REQUEST" != "false" -o "$TRAVIS_BRANCH" != "$SOURCE_BRANCH" ]; then
    echo "Skipping deploy; just doing a build."
    doCompile
    exit 0
fi

# Remove old generated data
cd $TRAVIS_BUILD_DIR

git checkout master

rm ./_symbols/*.md
rm ./_footprints/*.md
rm ./_packages3d/*.md
rm ./download/*

# Run generator scripts
cd ./_scripts

# Generate symbol data
python gen_symbol_info.py /home/travis/build/kicad-library/library/*.lib --schlib /home/travis/build/utils/schlib --output $TRAVIS_BUILD_DIR/_symbols --download $TRAVIS_BUILD_DIR/download/ --csv $TRAVIS_BUILD_DIR/_data/symbols.csv -v

# Generate footprint data
python gen_footprint_info.py /home/travis/build/footprints/*.pretty --script /home/travis/build/utils -v --download $TRAVIS_BUILD_DIR/download --output $TRAVIS_BUILD_DIR/_footprints

# Generate 3D model data
# python gen_3dmodel_info.py /home/travis/build/kicad-library/modules/packages3d/Capacitors_SMD.3dshapes --output $TRAVIS_BUILD_DIR/_packages3d

# And back to the build dir
cd $TRAVIS_BUILD_DIR
