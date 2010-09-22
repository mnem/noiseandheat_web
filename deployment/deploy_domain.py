#!/usr/bin/env python
# encoding: utf-8
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

import sys
import os
import shutil
import grp
import pwd
from optparse import OptionParser
from datetime import datetime

VERBOSE = False

VHOST_SECTION_TEMPLATE = """# Created %(timestamp)s
<VirtualHost *:80>
    DocumentRoot %(content)s
    ServerName %(domain)s
</VirtualHost>
"""

def log_verbose(message):
    """Logs a message to stdout if verbose output is enabled"""
    global VERBOSE
    if VERBOSE:
        print(message)

def log(message):
    """Logs a message to stdout"""
    print(message)

def fail(message):
    """Logs a fail message to stdout and terminates the program"""
    print("\n\n\a[FAIL] %s" % message)
    raise SystemExit

def create_folder_if_needed(path):
    """Creates the specified folder structure if it does not already exist"""
    if not os.path.isdir(path):
        log_verbose("Creating folders: %s" % path )
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno == 13:
                fail("I'm sorry Dave, I can't let you do that. Perhaps you should sudo this script.")
            else:
                raise e
    else:
        log_verbose("Folders already exist: %s" % path )

def delete_folder_if_exists(path):
    """Deletes the specified folder if it exists"""
    if os.path.isdir(path):
        log_verbose("Deleting folder: %s" % path )
        try:
            shutil.rmtree(path)
        except OSError as e:
            if e.errno == 13:
                fail("I'm sorry Dave, I can't let you do that. Perhaps you should sudo this script.")
            else:
                raise e
    log_verbose("Folder has been deleted: %s" % path )

def write_vhost_file(vhost_path, domain_content_path, domain):
    """Writes the virtual hosts file"""
    vhosts_filename = os.path.join(vhost_path, domain)
    
    if os.path.exists(vhosts_filename):
        log_verbose("Overwriting existing vhost file: %s" % vhosts_filename )
    else:
        log_verbose("Creating new vhost file: %s" % vhosts_filename )
    
    params = dict(
        timestamp = datetime.utcnow().isoformat(" "),
        content   = domain_content_path,
        domain    = domain
    )
    
    vhost_section = VHOST_SECTION_TEMPLATE % params
    
    log_verbose("Virtual host section: \n%s" % vhost_section )
    
    try:
        file = open(vhosts_filename, "w")
        file.write(vhost_section)
    except OSError as e:
        if e.errno == 13:
            fail("I'm sorry Dave, I can't let you do that. Perhaps you should sudo this script.")
        else:
            raise e
    finally:
        file.close();

def copy_files(source, destination):
    """Recursively copies files from one location to another"""
    log_verbose("Copying files from %s to %s" % (source, destination))
    shutil.copytree(source, destination)

def set_owner_and_group(path, owner, group):
    """Recursively set the owner and group for all items on the specified path"""
    try:
        owner_numeric = int(owner)
    except:
        try:
            owner_numeric = pwd.getpwnam(owner).pw_uid
        except KeyError:
            fail("User doesn't seem to exist: %s" % owner)
        
    try:
        group_numeric = int(group)
    except:
        try:
            group_numeric = grp.getgrnam(group).gr_gid
        except KeyError:
            fail("Group doesn't seem to exist: %s" % owner)
    
    log_verbose("chown %d:%d %s" % (owner_numeric, group_numeric, path))
    os.chown(path, owner_numeric, group_numeric)
    
    for root, dirs, files in os.walk(path):  
        for momo in dirs:
            item = os.path.join(root, momo)
            log_verbose("chown %d:%d %s" % (owner_numeric, group_numeric, item))
            os.chown(item, owner_numeric, group_numeric)
        for momo in files:
            item = os.path.join(root, momo)
            log_verbose("chown %d:%d %s" % (owner_numeric, group_numeric, item))
            os.chown(item, owner_numeric, group_numeric)

def deploy_domain(subdomain, www, vhosts, user, group, verbose):
    global VERBOSE
    VERBOSE = verbose

    domain_content_path = os.path.join(www, subdomain)

    log("-----[Deploying %s]" % subdomain)

    log_verbose("\n")
    log_verbose("Domain content path  : %s" % domain_content_path)
    log_verbose("Subdomain            : %s" % subdomain)
    log_verbose("Virtual hosts folder : %s" % vhosts)
    log_verbose("user:group           : %s:%s" % (user, group))
    log_verbose("\n")
    
    log("-----[Creating virtual host]")
    create_folder_if_needed(vhosts)
    
    write_vhost_file(vhosts, domain_content_path, subdomain)
    
    log("-----[Copying content]")
    delete_folder_if_exists(domain_content_path)
    
    copy_files("content", domain_content_path)
    
    log("-----[Updating permissions]")
    set_owner_and_group(domain_content_path, user, group)

def main():
    """Main entry point"""
    op = OptionParser("usage: %prog [options]")
    op.add_option("-s", "--subdomain", default="noiseandheat.com", help="The subdomain to create a vhost for. [%default]")
    op.add_option("-w", "--www", default="/var/www", help="Domains content root. The subdomain will be created as a folder on this path. [%default]")
    op.add_option("-V", "--vhosts", default="/etc/httpd/vhosts.d", help="Virtual hosts conf folder. [%default]")
    op.add_option("-u", "--user", default="apache", help="The owner to set for the content files. [%default]")
    op.add_option("-g", "--group", default="apache", help="The group to set for the content files. [%default]")
    op.add_option("-v", "--verbose", action="store_true", default=True, help="Enable verbose output. [%default]")
    opts, args = op.parse_args()
    
    do_deploy(subdomain = opts.subdomain, 
              www       = opts.www, 
              vhosts    = opts.vhosts, 
              user      = opts.user, 
              group     = opts.group, 
              verbose   = opts.verbose)


if __name__ == '__main__':
    main()
