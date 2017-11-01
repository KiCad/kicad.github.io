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


SHA=`git rev-parse --verify HEAD`

git config user.name "Travis CI"
git config user.email "$COMMIT_AUTHOR_EMAIL"

git add _symbols
git add _footprints
git add _packages3d
git add download

# If there are no changes to the compiled out (e.g. this is a README update) then just bail.
if git diff origin/master --quiet; then
    echo "No changes found; exiting."
    exit 0
fi

git commit -m "Autobuild by Travis: ${SHA}"

chmod 600 .id_rsa
eval `ssh-agent -s`

ssh-add .id_rsa

# And push back upstream!
git push https://github.com/KiCad/kicad.github.io master