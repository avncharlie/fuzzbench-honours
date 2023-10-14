''' Integration for pear (experiments) '''

import os
import shutil
import subprocess

from fuzzers import utils
from fuzzers.aflplusplus import fuzzer as aflplusplus_fuzzer

def build():
    ''' Build benchmark. '''

    # build benchmark
    os.environ['CC'] = 'clang'
    os.environ['CXX'] = 'clang++'
    os.environ['CFLAGS'] = ' '.join(utils.NO_SANITIZER_COMPAT_CFLAGS)
    cxxflags = [utils.LIBCPLUSPLUS_FLAG] + utils.NO_SANITIZER_COMPAT_CFLAGS
    os.environ['CXXFLAGS'] = ' '.join(cxxflags)
    os.environ['FUZZER_LIB'] = '/util/libAFLRewriteDriver.a'
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
