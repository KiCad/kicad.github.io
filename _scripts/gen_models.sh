# Generate 3D model listings

rm $TRAVIS_BUILD_DIR/_packages3d/*.md
python gen_3dmodel_info.py $TRAVIS_BUILD_DIR/kicad-library/modules/packages3d/*.3dshapes --output $TRAVIS_BUILD_DIR/_packages3d