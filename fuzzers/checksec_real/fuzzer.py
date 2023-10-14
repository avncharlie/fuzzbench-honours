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
    #shutil.copy('/afl/afl-fuzz', build_directory)

    # set compilers to AFL fast compilers
    os.environ['CC'] = 'clang'
    os.environ['CXX'] = 'clang++'

    # disable address santizer (to standardise benchmarks)
    os.environ['CFLAGS'] = ' '.join(utils.NO_SANITIZER_COMPAT_CFLAGS)
    cxxflags = [utils.LIBCPLUSPLUS_FLAG] + utils.NO_SANITIZER_COMPAT_CFLAGS
    os.environ['CXXFLAGS'] = ' '.join(cxxflags)

    # use same driver as other benchmarks
    os.environ['FUZZER_LIB'] = '/util/libAFLRewriteDriver.a'

    # finally build
    utils.build_benchmark()

    # find target
    target_binary_name = os.getenv('FUZZ_TARGET')
    target_binary_path = os.path.join(os.environ['OUT'], target_binary_name)
    if not os.path.isfile(target_binary_path):
        print('cannot find target binary :(')
        exit(1)
    print(f'Target binary: {target_binary_path}')

    os.system(f"checksec --file={target_binary_path}")
    exit(1)

def fuzz(input_corpus, output_corpus, target_binary):
    ''' run benchmark. '''
    aflplusplus_fuzzer.fuzz(input_corpus, output_corpus, target_binary)
