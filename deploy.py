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

import os
import glob
from optparse import OptionParser

import deployment
from deployment.subdomain import Subdomain

def deploy_subdomain(subdomain_config_root, subdomain):
    """Deploys a subdomain"""
    deployment.log.message("===== Deploying subdomain %s from %s" % (subdomain, subdomain_config_root))
    if os.path.isdir(subdomain_config_root):
        s = Subdomain(subdomain)
        s.write_virtual_host_file()
        s.copy_to_content(os.path.join(subdomain_config_root, "content"))
        for custom_step in glob.glob(os.path.join(subdomain_config_root, "*.py")):
            custom_step_module, ext = os.path.splitext(custom_step)
            print(">>>>>>>>> " + custom_step_module)
    else:
        deployment.log.message("Skipping %s because %s is not a directory" % (subdomain, subdomain_config_root))
    
def deploy_all(domains_directory):
    """Deploys all subdomains in the specifed folder"""
    deployment.log.message("Deploying all subdomains in %s" % domains_directory)
    
    for subdomain in os.listdir(domains_directory):
        full_subdomain_path = os.path.join(domains_directory, subdomain)
        if os.path.isdir(full_subdomain_path):
            deploy_subdomain(full_subdomain_path, subdomain)
    
def main():
    """Main entry point"""
    op = OptionParser("usage: %prog [options] <subdomains>")
    op.add_option("-s", "--subdomain_configs", default="subdomains", help="The folder all the subdomain configs live in. [%default]")
    op.add_option("-u", "--www_user", default="apache", help="The owner for the content files. [%default]")
    op.add_option("-g", "--www_group", default="apache", help="The group owner for the content files. [%default]")
    op.add_option("-o", "--output", default=None, help="Sets the output directory for testing purposes. [%default]")
    op.add_option("-v", "--verbose", default=False, action="store_true", help="Enable verbose output. [%default]")
    opts, args = op.parse_args()

    if opts.verbose:
        deployment.log.log_level = 0
    else:
        deployment.log.log_level = 1
    domains_directory = os.path.realpath(opts.subdomain_configs)
    deployment.server_config.www_user = opts.www_user
    deployment.server_config.www_group = opts.www_group
    
    if opts.output is not None:
        test_output = os.path.realpath(opts.output)
        if not os.path.isdir(test_output):
            os.makedirs(test_output)
        deployment.log.message("Forcing output to %s" % test_output)
        
        drive, tail = os.path.splitdrive(deployment.server_config.htdocs_root)
        deployment.server_config.htdocs_root = os.path.join(test_output, tail[1:])

        drive, tail = os.path.splitdrive(deployment.server_config.virtual_hosts_conf_root)
        deployment.server_config.virtual_hosts_conf_root = os.path.join(test_output, tail[1:])
    
    if len(args) == 0:
        deploy_all(domains_directory)
    else:
        for subdomain in args:
            deploy_subdomain(os.path.join(domains_directory, subdomain), subdomain)

if __name__ == '__main__':
    main()
