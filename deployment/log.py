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

class Log(object):
    """Simple logging class"""

    def __init__(self, verbose=True):
        self.verbose = verbose

    def message(self, text):
        """Logs a message to stdout"""
        print(text)
        
    def verbose(self, text):
        """Logs a message to stdout if verbose output is enabled"""
        if verbose:
            print(text)
        
    def fail(self, text):
        """Logs a fail message to stdout and terminates the program"""
        print("\n\n\a[FAIL] %s" % message)
        raise SystemExit
