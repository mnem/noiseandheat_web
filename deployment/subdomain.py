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

from shutil import copytree

import deployment
from deployment.utils import change_owner, remove_if_exists_but_keep_backup, ensure_directory_exists
from deployment.virtual_host import VirtualHost

class Subdomain(object):
    """Provides an interface to manipulate subdomains"""

    def __init__(self, subdomain):
        self.subdomain = subdomain
        self.content_path = deployment.server_config.content_path(self.subdomain)
        self.virtual_host = VirtualHost(self.subdomain)

    def write_virtual_host_file(self, alias_subdomain=None, alias_domain=None):
        self.virtual_host.write_conf(alias_subdomain, alias_domain)

    def set_content_filesystem_owner(self):
        change_owner(self.content_path,
                     deployment.server_config.www_user,
                     deployment.server_config.www_group)

    def copy_to_content(self, source_path, ignore=None):
        remove_if_exists_but_keep_backup(self.content_path)
        copytree(source_path,
                 self.content_path,
                 ignore)
        self.set_content_filesystem_owner()
