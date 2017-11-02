cd $TRAVIS_BUILD_DIR

SHA=`git rev-parse --verify HEAD`

git config user.name "Travis CI"
git config user.email "kicad.klc.bot@gmail.com"

git add _symbols
git add _footprints
git add _packages3d
git add download

# Debug info
git status

# If there are no changes to the compiled out (e.g. this is a README update) then just bail.
if git diff origin/master --quiet; then
    echo "No changes found; exiting."
    exit 0
fi

echo "Pushing changes to origin master"

git commit -m "Autobuild by Travis: ${SHA}"

chmod 600 travis_key
eval `ssh-agent -s`

ssh-add travis_key

export GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"

git remote set-url --push origin git@github.com:KiCad/kicad.github.io.git

# And push back upstream (must use SSH repo URL)
git push origin master -v --progress
