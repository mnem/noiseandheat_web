"""
Licensed under the MIT license:

    http://www.opensource.org/licenses/mit-license.php

Copyright (c) 2010 David Wagner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
import grp
import pwd
import shutil

import deployment

def change_owner(path, owner, group):
    """Recursively changes the path's owner and group membership to the
    specified values."""
    try:
        owner_numeric = int(owner)
    except ValueError:
        try:
            owner_numeric = pwd.getpwnam(owner).pw_uid
        except KeyError:
            raise ValueError("User doesn't seem to exist: %s" % owner)

    try:
        group_numeric = int(group)
    except ValueError:
        try:
            group_numeric = grp.getgrnam(group).gr_gid
        except KeyError:
            raise ValueError("Group doesn't seem to exist: %s" % group)

    def chown(target):
        deployment.log.message("change_owner %s:%s (%d:%d) %s" % (owner, group, owner_numeric, group_numeric, target), 0)
        os.chown(target, owner_numeric, group_numeric)
    
    chown(path)

    for root, dirs, files in os.walk(path):  
        for momo in dirs:
            chown(os.path.join(root, momo))
        for momo in files:
            chown(os.path.join(root, momo))

def ensure_directory_exists(directory):
    """Ensures that the directory exists"""
    if not os.path.isdir(directory):
        os.makedirs(directory)

def remove_if_exists_but_keep_backup(directory):
    """Removes a directory if it exists by renaming by appending the 
    first integer causing the name to be unique"""
    if os.path.isdir(directory):
        copy_number = 1
        while os.path.exists("%s.%d" % (directory, copy_number)):
            copy_number += 1
        new_name = "%s.%d" % (directory, copy_number)
        deployment.log.message("Moving folder out of the way: %s => %s" % (directory, new_name) ,0)
        os.rename(directory, new_name)
