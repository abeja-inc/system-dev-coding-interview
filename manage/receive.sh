#!/bin/bash

set -eu

if [[ $# -ne 4 ]]; then
    echo "Usage: $0 <submit_filepath> <submit_id> <working_directory> <media>"
    exit 1
fi

filepath=$1
id=$2
working_dir=$3
media=$4
filename=$(basename "$filepath")
SUBMIT_BRANCH=${SUBMIT_BRANCH:-submit}
NO_PUSH_REMOTE=${NO_PUSH_REMOTE:-false}

# ###################
# prepare working directory
# ###################

# extract zip file to the provided directory
unzip $filepath -d $working_dir > /dev/null
if [ ! -d "$working_dir/.git" ]; then
    echo "Error: .git directory does not exist in $working_dir"
    exit 1
fi

# ###################
# validate the git directory structure
# ###################

pushd $working_dir > /dev/null
# Check the required branches exist
if ! git show-ref --quiet --verify "refs/heads/$SUBMIT_BRANCH"; then
    echo "Error: Branch 'submit' does not exist"
    exit 1
fi
if ! git show-ref --quiet --verify "refs/heads/main"; then
    echo "Error: Branch 'main' does not exist"
    exit 1
fi
# Check if submit branch can be fast-forwarded to main
if ! git merge-base --is-ancestor main ${SUBMIT_BRANCH}; then
    echo "Error: ${SUBMIT_BRANCH} is not fast-forwarded to main"
    exit 1
fi
# check if the remote repositories are removed.
remotes=$(git remote)
if [ -n "$remotes" ]; then
    echo "Error: Remote repository exists"
    exit 1
fi

# ##################
# Manipulates git history for privacy
# ##################

function get_new_email(){
    local id=$1
    local media=$2
    echo "${media}-${id}@example.com"
}


function reset_to_original_commit(){
    local id=$1
    local media=$2
    local new_email=$(get_new_email $id $media)
    local head_commit=$(git log --format='%H %ae' | grep -v $new_email | head -n1 | awk '{print $1}')
    git reset ${head_commit} --hard
}

function get_candidate_emails(){
    local current_branch=$(git branch --show-current)
    git switch main > /dev/null
    local latest_main_commit_hash=$(git rev-parse HEAD)
    git switch $current_branch > /dev/null

    local emails=$(git log --pretty=format:"%ae" $latest_main_commit_hash..HEAD | sort -u)
    echo $emails
}

function rewrite_repo(){
    local id=$1
    local media=$2
    local emails=$(get_candidate_emails $id)
    local new_email=$(get_new_email $id $media)
    for email in $emails; do
        echo "Rewriting history with $email -> $new_email"
        git filter-branch --env-filter '
        OLD_EMAIL="'$email'"
        CORRECT_NAME="'$media'-'$id'"
        CORRECT_EMAIL="'$new_email'"
        if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
        then
            export GIT_COMMITTER_NAME="$CORRECT_NAME"
            export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
        fi
        if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
        then
            export GIT_AUTHOR_NAME="$CORRECT_NAME"
            export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
        fi
        ' -f --tag-name-filter cat -- --branches --tags
    done
}

echo "rewring git history for privacy"
git switch $SUBMIT_BRANCH >> /dev/null
rewrite_repo $id $media

echo "resetting main branch commit to the original commit"
git switch main >> /dev/null
reset_to_original_commit $id $media


# ##################
# Submit the code to private repo.
# ##################

if [ "$NO_PUSH_REMOTE" = "true" ]; then
    echo "NO_PUSH_REMOTE is set to true. Skip pushing to remote repository."
    exit 0
fi

echo "creating a private repository on GitHub to submit the code"
repo_name="abeja-inc/system-dev-coding-interview-submit-${media}-${id}"
gh repo create --private $repo_name
if [ $? -ne 0 ]; then
    echo "Failed to create repository: $repo_name"
    exit 1
fi
git remote add origin "git@github.com:${repo_name}.git"

git push origin main
git push origin submit

echo "creating a pull request"
git switch submit
gh pr create -B main --title "submit from a candidate" -b ''

echo "Successfully submitted the code. Please add right permission to the repository."
