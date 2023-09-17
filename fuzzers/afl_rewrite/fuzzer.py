''' Integration for afl-rewrite '''

import os
import shutil
import subprocess

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
    os.environ['FUZZER_LIB'] = '/afl-rewrite/util/libAFLRewriteDriver.a'
    utils.build_benchmark()

    # rewrite target
    target_binary_name = os.getenv('FUZZ_TARGET')
    target_binary_path = os.path.join(os.environ['OUT'], target_binary_name)

    if not os.path.isfile(target_binary_path):
        print('cannot find target binary :(')
        exit(1)

    print(f'Target binary: {target_binary_path}')
    nm_proc = subprocess.run(
        [
            'sh', '-c',
            f"nm '{target_binary_path}' | grep -i 'T afl_rewrite_driver_stdin_input'"
        ],
        stdout=subprocess.PIPE,
        check=True
    )
    target_func = '0x' + nm_proc.stdout.split()[0].decode('utf-8')

    print('Rewriting ...')
    try:
        os.environ['TARGET'] = target_binary_path
        os.environ['PERSISTENT_MODE_ADDR'] = target_func
        os.environ['FORKSERVER_INIT_ADDR'] = target_func
        os.environ['PERSISTENT_MODE_COUNT'] = '2147483647'
        os.system('make -C /afl-rewrite build-no-docker')

        # copy rewritten binary over original binary
        shutil.copy(f'/afl-rewrite/out/{target_binary_name}', target_binary_path)

    except subprocess.CalledProcessError as e:
        print(e.output.decode())
        exit(1)


def fuzz(input_corpus, output_corpus, target_binary):
    ''' run benchmark. '''
    aflplusplus_fuzzer.fuzz(input_corpus, output_corpus, target_binary)
