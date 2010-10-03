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
import json
from optparse import OptionParser

import deployment
from deployment.subdomain import Subdomain

def run_script(script, subdomain=None):
    path, scriptname = os.path.split(script)
    deployment.log.message("-- Running custom script %s" % scriptname)
    deployment.log.message("-- [Changing directory to %s]" % path)
    os.chdir(path)
    deployment.log.message_prefix = scriptname
    execfile(script, 
             globals(), 
             dict(subdomain=subdomain, 
                  server_config=deployment.server_config, 
                  log=deployment.log))
    deployment.log.message_prefix = None
    deployment.log.message("-- %s finished" % scriptname)

def deploy_subdomain(subdomain_config_root, subdomain):
    """Deploys a subdomain and executes any python files in the subdomain folder"""
    deployment.log.message("\n\n===== Deploying subdomain %s from %s" % (subdomain, subdomain_config_root))
    if os.path.isdir(subdomain_config_root):
        s = Subdomain(subdomain)
        s.write_virtual_host_file()
        s.copy_to_content(os.path.join(subdomain_config_root, "content"))
        for custom_step in glob.glob(os.path.join(subdomain_config_root, "*.py")):
            run_script(custom_step, subdomain=s)
    else:
        deployment.log.message("Skipping %s because %s is not a directory" % (subdomain, subdomain_config_root))

def deploy_subdomains(subdomains_directory, subdomains):
    before_deploy_script = os.path.join(subdomains_directory, "before_deploy.py")
    after_deploy_script = os.path.join(subdomains_directory, "after_deploy.py")
    
    if os.path.exists(before_deploy_script):
        run_script(before_deploy_script)
    
    for subdomain in subdomains:
        full_subdomain_path = os.path.join(subdomains_directory, subdomain)
        if os.path.isdir(full_subdomain_path):
            deploy_subdomain(full_subdomain_path, subdomain)
            
    if os.path.exists(after_deploy_script):
        run_script(after_deploy_script)
    
def main():
    """Main entry point"""
    op = OptionParser("usage: %prog [options] config_json <subdomains>")
    op.add_option("-v", "--verbose", default=False, action="store_true", help="Enable verbose output. [%default]")
    opts, args = op.parse_args()

    if opts.verbose:
        deployment.log.log_level = 0
    else:
        deployment.log.log_level = 1
    
    if len(args) < 1:
        op.print_help()
        raise SystemExit
    
    try:
        configuration = json.load(open(args[0]))
    except IOError, io_error:
        deployment.log.message("Can't seem to read file '%s'. %s" % (args[0], str(io_error)))
        raise SystemExit
    except ValueError, value_error:
        deployment.log.message("'%s' doesn't appear to be valid JSON. %s" % (args[0], str(value_error)))
        raise SystemExit
    
    domains_directory = os.path.realpath(configuration["subdomains_path"])
    
    deployment.server_config.domain = configuration["domain"]
    deployment.server_config.htdocs_root = configuration["htdocs_root"]
    deployment.server_config.virtual_hosts_conf_root = configuration["virtual_hosts_conf_root"]
    deployment.server_config.www_user = configuration["www_user"]
    deployment.server_config.www_group = configuration["www_group"]
    
    if len(args) == 1:
        subdomain_list = os.listdir(domains_directory)
        deployment.log.message("Deploying all subdomains in %s" % domains_directory)
    else:
        subdomain_list = args[1:]
        deployment.log.message("Deploying subdomains %s" % str(subdomain_list))
    deploy_subdomains(domains_directory, subdomain_list)

if __name__ == '__main__':
    main()
