import os
import sys
import shutil
import tempfile
import subprocess
from distutils.dir_util import copy_tree
import json
import site

config_file = 'deploy-config.json'

with open('deploy-config.json') as f:
    config = json.load(f)


# Create temporary directory
temporary_directory = tempfile.gettempdir() + '\\deployment-build_' + config['repository']['name']
if os.path.exists(temporary_directory):
    try:
        shutil.rmtree(temporary_directory)
    except PermissionError:
        print('Please delete the directory at {0}'.format(temporary_directory))
        os.startfile(temporary_directory, operation='explore')
        sys.exit(1)
os.makedirs(temporary_directory)
print('[Deploy] Using: ' + temporary_directory)


# Gather versioning
config['versioning']['build'] += 1
next_build = config['versioning']['build']
version = config['versioning']['version']


# Build project
print('[Deploy] Building project')
os.environ['build'] = str(next_build)
site.build()


# Clone branch
print('[Deploy] Cloning branch')
username = config['repository']['auth']['username'] or input('Username: ')
password = config['repository']['auth']['password'] or input('Password: ')
git_repo = config['repository']['upstream']
url = git_repo.split('://')[0] + '://' + username + ':' + password.replace('@', '%40') + '@' + git_repo.split('://')[1]
process = subprocess.Popen(
    ['git', 'clone', '-b', 'gh-pages', '--single-branch', url],
    stdout=subprocess.PIPE,
    cwd=temporary_directory,
    universal_newlines=True,
    shell=True
)
for stdout_line in iter(process.stdout.readline, ""):
    print(stdout_line, end='')
process.stdout.close()
process.wait()


# Clear previous build from repo
print('[Deploy] Clearing previous build')
cloned_git_root_dir = temporary_directory + '\\' + config['repository']['name'] + '\\'
for entry in [i for i in os.listdir(cloned_git_root_dir) if i not in ['.git'] + config['repository']['ignore']]:
    if os.path.isfile(cloned_git_root_dir + entry):
        os.remove(cloned_git_root_dir + entry)
    else:
        shutil.rmtree(cloned_git_root_dir + entry)


# Move into repo
print('[Deploy] Copying build')
build_dir = config['project']['build']
copy_tree(build_dir, cloned_git_root_dir)


# Stage
print('[Deploy] Staging commit')
process = subprocess.Popen(
    ['git', 'add', '-A'],
    stdout=subprocess.PIPE,
    cwd=cloned_git_root_dir,
    universal_newlines=True,
    shell=True
)
for stdout_line in iter(process.stdout.readline, ""):
    print(stdout_line, end='')
process.stdout.close()
process.wait()


# Check if there have been changes made
print('[Deploy] Checking for changes')
process = subprocess.Popen(
    ['git', 'status'],
    stdout=subprocess.PIPE,
    cwd=cloned_git_root_dir,
    universal_newlines=True,
    shell=True
)
out, err = process.communicate()
if 'nothing to commit, working tree clean' not in out:
    print('[Deploy] Changes detected')
    print(out)

    # Commit
    print('[Deploy] Committing')
    process = subprocess.Popen(
        ['git', 'commit', '-m', 'Version:{} Build:{}'.format(version, next_build)],
        stdout=subprocess.PIPE,
        cwd=cloned_git_root_dir,
        universal_newlines=True,
        shell=True
    )
    out, err = process.communicate()
    print(out)

    # Tag
    print('[Deploy] Tagging')
    tag = '{}+{}'.format(version, next_build)
    print('[Deploy] Tag: ' + tag)
    process = subprocess.Popen(
        ['git', 'tag', tag],
        stdout=subprocess.PIPE,
        cwd=cloned_git_root_dir,
        universal_newlines=True,
        shell=True
    )
    process.wait()

    # Push
    question = input('Do you want to push? ')
    if question.lower() in ['yes', 'y', 'yea']:
        print('[Deploy] Pushing')
        process = subprocess.Popen(
            ['git', 'push'],
            stdout=subprocess.PIPE,
            cwd=cloned_git_root_dir,
            universal_newlines=True,
            shell=True
        )
        for stdout_line in iter(process.stdout.readline, ""):
            print(stdout_line, end='')
        process.stdout.close()
        process.wait()

        print('[Deploy] Pushing tag')
        process = subprocess.Popen(
            ['git', 'push', 'origin', tag],
            stdout=subprocess.PIPE,
            cwd=cloned_git_root_dir,
            universal_newlines=True,
            shell=True
        )
        for stdout_line in iter(process.stdout.readline, ""):
            print(stdout_line, end='')
        process.stdout.close()
        process.wait()

    # Save build version
    print('[Deploy] Saving build version')
    with open(config_file, 'w') as outfile:
        json.dump(config, outfile, indent=4, sort_keys=True)

else:
    print('[Deploy] No changes detected')


# Clear build
print('[Deploy] Clearing build')
shutil.rmtree(build_dir)

# Delete push environment
question = input('Delete push environment? ')
if question.lower() in ['yes', 'y', 'yea']:
    shutil.rmtree(temporary_directory)
