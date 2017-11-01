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

echo "Pushing changes to origin master"

git commit -m "Autobuild by Travis: ${SHA}"

chmod 600 .id_rsa
eval `ssh-agent -s`

ssh-add .id_rsa

# And push back upstream!
git push https://github.com/KiCad/kicad.github.io master
