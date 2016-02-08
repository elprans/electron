#!/usr/bin/env python

import os
import subprocess
import sys

SOURCE_ROOT = os.path.dirname(os.path.dirname(__file__))


def main():
  node = sys.argv[1]
  args = sys.argv[2:]

  call_browserify(node, args)


def call_browserify(node, args):
  browserify = os.path.join(
    SOURCE_ROOT, 'node_modules', '.bin', 'browserify')
  subprocess.check_call([node, browserify] + args)


if __name__ == '__main__':
  sys.exit(main())
