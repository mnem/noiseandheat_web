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

from deployment import log

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
        log.verbose("change_owner %d:%d %s" % (owner, group, target))
        os.chown(target, owner, group)
    
    chown(path)

    for root, dirs, files in os.walk(path):  
        for momo in dirs:
            chown(os.path.join(root, momo))
        for momo in files:
            chown(os.path.join(root, momo))
