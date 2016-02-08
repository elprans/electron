{
  'variables': {
    # Clang stuff.
    'make_clang_dir%': 'vendor/llvm-build/Release+Asserts',
    # Set this to true when building with Clang.
    'clang%': 1,

    'variables': {
      # The minimum macOS SDK version to use.
      'mac_sdk_min%': '10.10',

      # Set ARM architecture version.
      'arm_version%': 7,

      # Set NEON compilation flags.
      'arm_neon%': 1,

      # Abosulte path to source root.
      'source_root%': '<!(python <(DEPTH)/tools/atom_source_root.py)',
    },

    # Copy conditionally-set variables out one scope.
    'mac_sdk_min%': '<(mac_sdk_min)',
    'arm_version%': '<(arm_version)',
    'arm_neon%': '<(arm_neon)',
    'source_root%': '<(source_root)',

    # Variables to control Link-Time Optimization (LTO).
    'use_lto%': 0,
    'use_lto_o2%': 0,

    'conditions': [
      # Do not use Clang on Windows.
      ['OS=="win"', {
        'clang%': 0,
      }],  # OS=="win"

      # Search for the available version of SDK.
      ['OS=="mac"', {
        'mac_sdk%': '<!(python <(DEPTH)/tools/mac/find_sdk.py <(mac_sdk_min))',
      }],

      # Set default compiler flags depending on ARM version.
      ['arm_version==6', {
        'arm_arch%': 'armv6',
        'arm_tune%': '',
        'arm_fpu%': 'vfp',
        'arm_float_abi%': 'softfp',
        'arm_thumb%': 0,
      }],  # arm_version==6
      ['arm_version==7', {
        'arm_arch%': 'armv7-a',
        'arm_tune%': 'generic-armv7-a',
        'conditions': [
          ['arm_neon==1', {
            'arm_fpu%': 'neon',
          }, {
            'arm_fpu%': 'vfpv3-d16',
          }],
        ],
        'arm_float_abi%': 'hard',
        'arm_thumb%': 1,
      }],  # arm_version==7
    ],
  },
  'conditions': [
    # Setup building with clang.
    ['clang==1', {
      'make_global_settings': [
        ['CC', '<(make_clang_dir)/bin/clang'],
        ['CXX', '<(make_clang_dir)/bin/clang++'],
        ['CC.host', '$(CC)'],
        ['CXX.host', '$(CXX)'],
      ],
      'target_defaults': {
        'cflags_cc': [
          '-std=c++11',
        ],
        'xcode_settings': {
          'CC': '<(make_clang_dir)/bin/clang',
          'LDPLUSPLUS': '<(make_clang_dir)/bin/clang++',
          'OTHER_CFLAGS': [
            '-fcolor-diagnostics',
          ],

          'GCC_C_LANGUAGE_STANDARD': 'c99',  # -std=c99
          'CLANG_CXX_LIBRARY': 'libc++',  # -stdlib=libc++
          'CLANG_CXX_LANGUAGE_STANDARD': 'c++11',  # -std=c++11
        },
        'target_conditions': [
          ['_type in ["executable", "shared_library"]', {
            'xcode_settings': {
              # On some machines setting CLANG_CXX_LIBRARY doesn't work for
              # linker.
              'OTHER_LDFLAGS': [ '-stdlib=libc++' ],
            },
          }],
        ],
      },
    }],  # clang==1

    # Specify the SDKROOT.
    ['OS=="mac"', {
      'target_defaults': {
        'xcode_settings': {
          'SDKROOT': 'macosx<(mac_sdk)',  # -isysroot
        },
      },
    }],

    # Setup cross-compilation on Linux.
    ['OS=="linux"', {
      'target_defaults': {
        'target_conditions': [
          ['target_arch=="ia32" and _toolset=="target"', {
            'asflags': [
              '-32',
            ],
            'cflags': [
              '-msse2',
              '-mfpmath=sse',
              '-mmmx',  # Allows mmintrin.h for MMX intrinsics.
              '-m32',
            ],
            'ldflags': [
              '-m32',
            ],
          }],  # target_arch=="ia32" and _toolset=="target"
          ['target_arch=="x64" and _toolset=="target"', {
            'cflags': [
              '-m64',
              '-march=x86-64',
            ],
            'ldflags': [
              '-m64',
            ],
            'conditions': [
              ['use_lto==1 and clang==0', {
                'cflags': [
                  '-fno-fat-lto-objects',
                  '-fuse-linker-plugin',
                  '-flto=4',
                  '--param=lto-partitions=1',
                ],
                'ldflags': [
                  '-fno-fat-lto-objects',
                  '-fuse-linker-plugin',
                  '-flto=4',
                  '--param=lto-partitions=1',
                ],
                'arflags': [
                  '<!@(python <(DEPTH)/tools/ar-flags.py)',
                ]
              }],
              ['use_lto==1 and clang==1', {
                'cflags': [
                  '-flto',
                  '-fwhole-program-vtables'
                ],
                'ldflags': [
                  '-flto',
                  '-fwhole-program-vtables'
                ],
              }],
            ],
          }],  # target_arch=="x64" and _toolset=="target"
          ['target_arch=="arm" and _toolset=="target"', {
            'conditions': [
              ['clang==0', {
                'cflags_cc': [
                  '-Wno-abi',
                ],
              }],
              ['clang==1 and arm_arch!=""', {
                'cflags': [
                  '-target arm-linux-gnueabihf',
                ],
                'ldflags': [
                  '-target arm-linux-gnueabihf',
                ],
              }],
              ['arm_arch!=""', {
                'cflags': [
                  '-march=<(arm_arch)',
                ],
                'conditions': [
                  ['use_lto==1 or use_lto_o2==1', {
                    'ldflags': [
                      '-march=<(arm_arch)',
                    ],
                  }],
                ],
              }],
              ['arm_tune!=""', {
                'cflags': [
                  '-mtune=<(arm_tune)',
                ],
                'conditions': [
                  ['use_lto==1 or use_lto_o2==1', {
                    'ldflags': [
                      '-mtune=<(arm_tune)',
                    ],
                  }],
                ],
              }],
              ['arm_fpu!=""', {
                'cflags': [
                  '-mfpu=<(arm_fpu)',
                ],
                'conditions': [
                  ['use_lto==1 or use_lto_o2==1', {
                    'ldflags': [
                      '-mfpu=<(arm_fpu)',
                    ],
                  }],
                ],
              }],
              ['arm_float_abi!=""', {
                'cflags': [
                  '-mfloat-abi=<(arm_float_abi)',
                ],
                'conditions': [
                  ['use_lto==1 or use_lto_o2==1', {
                    'ldflags': [
                      '-mfloat-abi=<(arm_float_abi)',
                    ],
                  }],
                ],
              }],
              ['arm_thumb==1', {
                'cflags': [
                  '-mthumb',
                ],
                'conditions': [
                  ['use_lto==1 or use_lto_o2==1', {
                    'ldflags': [
                      '-mthumb',
                    ],
                  }],
                ],
              }],
            ],
          }],  # target_arch=="arm" and _toolset=="target"
        ],
      },
    }],  # OS=="linux"
  ],
}
