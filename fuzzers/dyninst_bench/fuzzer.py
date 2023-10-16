''' Integration for pear (experiments) '''

import os
import shutil

from fuzzers import utils
from fuzzers.aflplusplus import fuzzer as aflplusplus_fuzzer


def build():
    ''' Build benchmark. '''
    build_directory = os.environ['OUT']

    # move fuzzer to build directory
    shutil.copy('/afl/afl-fuzz', build_directory)

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

    # instrument and replace target 
    gen_file = f'{target_binary_path}.dyninst.afl'
    cmd = f'afl-dyninst -i {target_binary_path} -o {gen_file} -x'

    print(f'Adding instrumentation (running command: {cmd}) ...')
    os.system(cmd)

    if os.path.isfile(f'{gen_file}'):
        os.system(f'cp {gen_file} {target_binary_path}')
    else:
        print('dyninst transform failed!')
        exit(1)


def fuzz(input_corpus, output_corpus, target_binary):
    ''' run benchmark. '''
    os.environ['AFL_SKIP_BIN_CHECK'] = '1'
    aflplusplus_fuzzer.fuzz(input_corpus, output_corpus, target_binary)
