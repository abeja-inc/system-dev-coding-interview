#!/bin/bash

set -eu -o pipefail

SUBMIT_BRANCH=${SUBMIT_BRANCH:-submit}
IGNORE_UNCOMMITTED=${IGNORE_UNCOMMITTED:-false}

# Check if the current directory is a Git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "Not in a Git repository. Aborting..."
    exit 1
fi

# Check for uncommitted files
if [[ "$IGNORE_UNCOMMITTED" != "true" ]]; then
    if git status --porcelain | grep -E '^(M| M|A|D| U|\?\?)' >/dev/null 2>&1; then
        echo "Uncommitted files found:"
        git status --porcelain | awk '{print " - " $2}'
        echo "Aborting..."
        exit 1
    fi
else
    echo "Ignoring uncommitted files..."
fi

# Check for branch names

current_branch=$(git rev-parse --abbrev-ref HEAD)
if [[ "$current_branch" != "$SUBMIT_BRANCH" ]]; then
    echo "Not on '${SUBMIT_BRANCH}' branch. Aborting..."
    exit 1
fi

# Check if current branch can be fast-forwarded to main
if ! git merge-base --is-ancestor main ${SUBMIT_BRANCH}; then
    echo "Error: ${SUBMIT_BRANCH} is not fast-forwarded to main"
    exit 1
fi

echo "success validation"

# Run test
make docker-build
make docker-run

# archive target files

temp_dir=$(mktemp -d)

# Copy files respecting .gitignore patterns
rsync -a --exclude-from=../../.gitignore --exclude-from=.gitignore ../.. "$temp_dir"
echo "copied target files to $temp_dir"

pushd "$temp_dir" > /dev/null

# Remove remote repositories
remote_repositories=$(git remote)
for remote_repo in $remote_repositories; do
    git remote remove "$remote_repo"
done

# zip directory
zip_filename="submit.zip"
zip -r $zip_filename . > /dev/null
echo "zip success"

popd > /dev/null

mv "$temp_dir/$zip_filename" .

echo "success archive $zip_filename"
