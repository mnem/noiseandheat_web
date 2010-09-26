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

from deployment.utils import change_owner

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
            conf_filename = server_config.virtual_host_conf_filename(self.subdomain)
        else:
            conf_filename = server_config.virtual_host_conf_filename(override_subdomain)
        
        content_path = server_config.content_path(self.subdomain)

        if os.path.exists(conf_filename):
            log.verbose("Overwriting existing vhost file: %s" % conf_filename )
        else:
            log.verbose("Creating new vhost file: %s" % conf_filename )

        params = dict(
            timestamp = datetime.utcnow().isoformat(" "),
            content   = content_path,
            domain    = self.subdomain
        )
        virtual_host_section = _VIRTUAL_HOST_SECTION_TEMPLATE % params
        log.verbose("Virtual host section:\n%s" % virtual_host_section )

        try:
            file = open(conf_filename, "w")
            file.write(virtual_host_section)
            file.close();
            change_owner(conf_filename, 
                         server_config.www_user, 
                         server_config.www_group)
        except IOError as e:
            if e.errno == 13:
                log.fail("Cannot write to file. "
                         "Perhaps you should sudo this script.")
            else:
                raise e
        
