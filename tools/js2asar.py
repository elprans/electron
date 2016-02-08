#!/usr/bin/env python

import errno
import os
import shutil
import subprocess
import sys
import tempfile

SOURCE_ROOT = os.path.dirname(os.path.dirname(__file__))


def main():
  node = sys.argv[1]
  archive = sys.argv[2]
  folder_name = sys.argv[3]
  source_files = sys.argv[4:]

  output_dir = tempfile.mkdtemp()
  copy_files(source_files, output_dir)
  call_asar(node, archive, os.path.join(output_dir, folder_name))
  shutil.rmtree(output_dir)


def copy_files(source_files, output_dir):
  for source_file in source_files:
    output_path = os.path.join(output_dir, source_file)
    safe_mkdir(os.path.dirname(output_path))
    shutil.copy2(source_file, output_path)


def call_asar(node, archive, output_dir):
  asar = os.path.join(SOURCE_ROOT, 'node_modules', '.bin', 'asar')
  if sys.platform in ['win32', 'cygwin']:
    asar += '.cmd'
  subprocess.check_call([node, asar, 'pack', output_dir, archive])


def safe_mkdir(path):
  try:
    os.makedirs(path)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise


if __name__ == '__main__':
  sys.exit(main())
