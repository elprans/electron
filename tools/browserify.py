#!/usr/bin/env python

import os
import subprocess
import sys

SOURCE_ROOT = os.path.dirname(os.path.dirname(__file__))


def main():
  node = sys.argv[1]
  source = sys.argv[2]
  output = sys.argv[3]

  call_browserify(node, source, output)


def call_browserify(node, source, output):
  browserify = os.path.join(
    SOURCE_ROOT, 'node_modules_browserify', '.bin', 'browserify')
  subprocess.check_call([node, browserify, source, '-o', output])


if __name__ == '__main__':
  sys.exit(main())
