#!/usr/bin/env python

# This script performs the following operations on the PSS GIT repository:
# ------------------------------------------------------------------------------
# 1. Make a copy of master branch as develop
# 2. Recreate master from v16.2 branch
# 3. Rename all release branches prefixing them with a 'Release/'
# 4. Rename all feature branches prefixing them with a 'Feature/' and JIRA ID
# ------------------------------------------------------------------------------
# Author: Ranjith Karunakaran

import subprocess, sys
def system(*args, **kwargs):
    """Run shell command and capture output"""
    print "Running: " + (" ".join(str(s) for s in args))
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, err = proc.communicate()
    proc.wait()
    if proc.returncode != 0:
        print "Error running command, exiting script"
        sys.exit()
    return out

def rename_branch(oldname, newname):
    """rename branch oldname to newname"""
    cmds = [['git', 'checkout', oldname],
            ['git', 'branch', '-m', oldname, newname],
            ['git', 'push', 'origin', '--delete', oldname],
            ['git', 'push', 'origin', newname]]
    for cmd in cmds:
        system(**cmd)

def copy_branch(newbranch, srcbranch):
    """copy branch srcbranch to newbranch"""
    system('git', 'checkout', srcbranch)
    system('git', 'checkout','-b', newbranch)
    system('git', 'push', '-u', 'origin', newbranch)

def replace_master_with(branch):
    """replace master from a branch, retaining history"""
    system('git', 'checkout', branch)
    system('git', 'merge', '--strategy=ours','master')
    system('git', 'checkout', 'master')
    system('git', 'merge', branch)
    system('git', 'push', '-f', 'origin', 'master')

def perform_changes():
    """perform branch copies and renames"""

    # prepare master branch
    copy_branch('develop','master')
    replace_master_with('v16.2')

    # rename release branches
    release_branches = ['v16', 'v15', 'v16.2', 'v15.2_CR', 'v16.1', 'v14', 'v15.1_CR', 'v14_3_3', 'v14.0.1']
    for branch in release_branches:
        rename_branch(branch, 'release/' + branch)

    # rename feature branches
    feature_branches = [('angular2UI', 'feature/PS-7923-angular2UI'),
                        ('angularUI', 'feature/PS-6364-angularUI'),
                        ('highcharts', 'feature/PS-6371-highcharts'),
                        ('V16_lucene_upgrade', 'feature/PS-5151-V16_lucene_upgrade'),
                        ('scalability', 'feature/scalability'),
                        ('codecleanup', 'feature/codecleanup'),
                        ('ComSciPOC', 'feature/ComSciPOC')]
    for oldname, newname in feature_branches:
        rename_branch(oldname, newname)

# run changes
if __name__ == "__main__":
    perform_changes()