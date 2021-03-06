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
import subprocess
import tempfile
import os

# Locals supplied to the file:
#   subdomain: subdomain object for this subdomain
#   server_config: server_config object
#   log: log object
log.message("Downloading latest wordpress")
if not os.path.exists("latest.zip"):
    subprocess.Popen("wget http://wordpress.org/latest.zip", shell=True).wait()
    subprocess.Popen("unzip latest.zip -d '%s'" % subdomain.content_path, shell=True).wait()
else:
    log.message("There's already a wordpress archive downloaded, skipping download and extract. If you want to download it again, delete '%s'" % os.path.abspath("latest.zip"))

if not os.path.exists("salt.txt"):
    subprocess.Popen("wget https://api.wordpress.org/secret-key/1.1/salt/ -O salt.txt", shell=True).wait()
else:
    log.message("There's already a wordpress salt file downloaded, skipping download. If you want to download it again, delete '%s'" % os.path.abspath("salt.txt"))
