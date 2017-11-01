# Generate footprint listings

python gen_footprint_info.py /home/travis/build/footprints/*.pretty --script /home/travis/build/utils -v --download $TRAVIS_BUILD_DIR/download/ --output $TRAVIS_BUILD_DIR/_footprints
