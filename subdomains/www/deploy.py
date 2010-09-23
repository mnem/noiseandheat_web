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
from optparse import OptionParser

this_script_dir=os.path.dirname(os.path.realpath(__file__))
deployment_module_path = os.path.join(this_script_dir, "..", "..")
sys.path.append(deployment_module_path)
from deployment.deploy_domain import deploy_domain
from deployment.deploy_domain import write_vhost_file

#############################################
# Defaults for the command line arguments
SUBDOMAIN = "noiseandheat.com"
CONTENT   = os.path.join(this_script_dir, "content")
WWW       = "/var/www"
VHOSTS    = "/etc/httpd/vhosts.d"
USER      = "apache"
GROUP     = "apache"
VERBOSE   = False

#############################################
# Parse command line
op = OptionParser("usage: %prog [options]")
op.add_option("-s", "--subdomain", default=SUBDOMAIN, help="The subdomain to create a vhost for. [%default]")
op.add_option("-c", "--content", default=CONTENT, help="The content to copy. [%default]")
op.add_option("-w", "--www", default=WWW, help="Domains content root. The subdomain will be created as a folder on this path. [%default]")
op.add_option("-V", "--vhosts", default=VHOSTS, help="Virtual hosts conf folder. [%default]")
op.add_option("-u", "--user", default=USER, help="The owner to set for the content files. [%default]")
op.add_option("-g", "--group", default=GROUP, help="The group to set for the content files. [%default]")
op.add_option("-v", "--verbose", default=VERBOSE, action="store_true", help="Enable verbose output. [%default]")
opts, args = op.parse_args()

#############################################
# Start the deployment
deploy_domain(subdomain = opts.subdomain,
              content   = opts.content, 
              www       = opts.www, 
              vhosts    = opts.vhosts, 
              user      = opts.user, 
              group     = opts.group, 
              aliases   = ["www.noiseandheat.com"],
              verbose   = opts.verbose)
