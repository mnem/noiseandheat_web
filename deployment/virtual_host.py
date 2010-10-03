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
from datetime import datetime

import deployment
from deployment.utils import change_owner, ensure_directory_exists

class VirtualHost(object):
    """Class allowing the creation of a virtual host configuration file
    for an apache server."""

    def __init__(self, subdomain):
        if subdomain is None:
            raise ValueError("subdomain can't be None")
        self.subdomain = subdomain

    def write_conf(self, override_subdomain=None):
        """Writes the virtual host configuration file to the configuration
        directory specified by the server_configuration object"""
        if override_subdomain is None:
            conf_filename = deployment.server_config.virtual_host_conf_filename(self.subdomain)
            domain_name = deployment.server_config.full_domain_name(self.subdomain)
        else:
            conf_filename = deployment.server_config.virtual_host_conf_filename(override_subdomain)
            domain_name = deployment.server_config.full_domain_name(override_subdomain)
        
        content_path = deployment.server_config.content_path(self.subdomain)

        if os.path.exists(conf_filename):
            deployment.log.message("Overwriting existing vhost file: %s" % conf_filename, 0)
        else:
            deployment.log.message("Creating new vhost file: %s" % conf_filename, 0)

        params = dict(
            timestamp = datetime.utcnow().isoformat(" "),
            content   = content_path,
            domain    = domain_name
        )
        virtual_host_section = VirtualHost._VIRTUAL_HOST_SECTION_TEMPLATE % params
        deployment.log.message("Virtual host section:\n%s" % virtual_host_section, 0)

        try:
            ensure_directory_exists(deployment.server_config.virtual_hosts_conf_root)
            file = open(conf_filename, "w")
            file.write(virtual_host_section)
            file.close();
            change_owner(conf_filename, 
                         deployment.server_config.www_user, 
                         deployment.server_config.www_group)
        except IOError as e:
            if e.errno == 13:
                deployment.log.fail("Cannot write to file. "
                                    "Perhaps you should sudo this script.")
            else:
                raise e
        
    _VIRTUAL_HOST_SECTION_TEMPLATE = ("# Created %(timestamp)s\n"
                                      "<VirtualHost *:80>\n"
                                      "    DocumentRoot %(content)s\n"
                                      "    ServerName %(domain)s\n"
                                      "</VirtualHost>\n")
