#!/usr/bin/env python

import os
import subprocess

if __name__ == '__main__':
    cc = os.environ.get('CC', '/usr/bin/cc')
    gcc_version = subprocess.check_output(
        [cc, '-dumpversion'], universal_newlines=True).strip(' \n')

    lto_plugin = os.path.join(
        '/usr/libexec/gcc/x86_64-pc-linux-gnu/', gcc_version,
        'liblto_plugin.so')

    print('--plugin={}'.format(lto_plugin))
