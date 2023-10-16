''' Integration for aflplusplus '''

import os
import shutil
from collections import namedtuple

from fuzzers import utils
from fuzzers.aflplusplus import fuzzer as aflplusplus_fuzzer

def build():
    ''' Build benchmark. '''
    build_directory = os.environ['OUT']

    # move fuzzer to build directory
    shutil.copy('/afl/afl-fuzz', build_directory)

    # set options for LTO compiler
    os.environ['CC'] = '/afl/afl-clang-lto'
    os.environ['CXX'] = '/afl/afl-clang-lto++'
    if os.path.isfile('/usr/local/bin/llvm-ranlib-13'):
        os.environ['RANLIB'] = 'llvm-ranlib-13'
        os.environ['AR'] = 'llvm-ar-13'
        os.environ['AS'] = 'llvm-as-13'
    elif os.path.isfile('/usr/local/bin/llvm-ranlib-12'):
        os.environ['RANLIB'] = 'llvm-ranlib-12'
        os.environ['AR'] = 'llvm-ar-12'
        os.environ['AS'] = 'llvm-as-12'
    else:
        os.environ['RANLIB'] = 'llvm-ranlib'
        os.environ['AR'] = 'llvm-ar'
        os.environ['AS'] = 'llvm-as'

    # disable address santizer (to standardise benchmarks)
    os.environ['CFLAGS'] = ' '.join(utils.NO_SANITIZER_COMPAT_CFLAGS)
    cxxflags = [utils.LIBCPLUSPLUS_FLAG] + utils.NO_SANITIZER_COMPAT_CFLAGS
    os.environ['CXXFLAGS'] = ' '.join(cxxflags)

    # disable optimisation (to standardise benchmarks)
    os.environ["AFL_DONT_OPTIMIZE"] = '1'

    # set map size to 64k (to standardise benchmarks)
    os.environ['AFL_MAP_SIZE'] = '65536'

    # use same driver as other benchmarks
    os.environ['FUZZER_LIB'] = '/util/libAFLRewriteDriver.a'

    # finally build
    utils.build_benchmark()

def fuzz(input_corpus, output_corpus, target_binary):
    ''' run benchmark. '''
    aflplusplus_fuzzer.fuzz(input_corpus, output_corpus, target_binary)
