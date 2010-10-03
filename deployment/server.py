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
import subprocess

import deployment

class ServerConfiguration(object):
    """Holds the basic configuration information describing a server setup."""

    def __init__(self, domain="noiseandheat.com",
                       htdocs_root="/var/www",
                       virtual_hosts_conf_root="/etc/httpd/vhosts.d",
                       www_user="apache", www_group="apache"):
        self.domain = domain
        self.htdocs_root = htdocs_root
        self.virtual_hosts_conf_root = virtual_hosts_conf_root
        self.www_user = www_user
        self.www_group = www_group

    def full_domain_name(self, subdomain):
        """Returns the full domain name."""
        subdomain_len = len(subdomain)
        if subdomain_len == 0:
            return self.domain
        elif subdomain[-1] == ".":
            return subdomain  + self.domain
        else:
            return subdomain + "." + self.domain

    def virtual_host_conf_filename(self, subdomain):
        """Returns the filename for the virtual host configuration for the
        subdomain."""
        return os.path.join(self.virtual_hosts_conf_root,
                            self.full_domain_name(subdomain) + ".vhost")

    def content_path(self, subdomain):
        """Returns the base bath for the content for the subdomain."""
        return os.path.join(self.htdocs_root, self.full_domain_name(subdomain))
        
    def restart(self):
        """Attempts to restart the http server using a couple of commands"""
        for restart_command in self._HTTPD_RESTART_COMMANDS:
            deployment.log.message("\nTrying to restart httpd with '%s'" % restart_command)
            p = subprocess.Popen(restart_command, shell=True)
            p.wait()
            if p.returncode == 0:
                deployment.log.message("httpd restarted, I think.")
                return
            else:
                deployment.log.message("Command failed with code %d. Trying another way." % p.returncode)
        deployment.log.message("Giving up trying to restart httpd. You'll have to do it yourself.")
        
    _HTTPD_RESTART_COMMANDS = ["sudo service httpd restart",
                               "sudo apachectl restart",
                               "sudo apache2ctl restart"]
