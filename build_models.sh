
# Pull requests and commits to other branches shouldn't try to deploy, just build to verify
if [ "$TRAVIS_PULL_REQUEST" != "false" -o "$TRAVIS_BRANCH" != "master" ]; then
    echo "Skipping deploy; just doing a build."
    exit 0
fi

# Remove old generated data
cd $TRAVIS_BUILD_DIR

rm _packages3d/*.md

# Generate 3D model data
python _scripts/gen_3dmodel_info.py /home/travis/build/kicad-library/modules/packages3d/*.3dshapes --output $TRAVIS_BUILD_DIR/_packages3d --download $TRAVIS_BUILD_DIR/download -v
