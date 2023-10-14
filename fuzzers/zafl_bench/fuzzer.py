''' Integration for pear (experiments) '''

import os
import shutil
import subprocess

from fuzzers import utils
from fuzzers.aflplusplus import fuzzer as aflplusplus_fuzzer

def set_env(script):
    '''
    Run a script that sets environment variables, then set those environment
    variables in current environment
    '''
    init_env = dict(os.environ)

    # run script
    command = f"bash -c 'source {script} && env'"
    output = subprocess.check_output(command, shell=True, universal_newlines=True)

    # parse environment variables
    new_env = {}
    for line in output.split('\n'):
        if '=' in line:
            key, value = line.split('=', 1)
            new_env[key] = value

    # set new and updated environment variables in current env
    for var in new_env:
        if (not var in init_env) or init_env[var] != new_env[var]:
            os.environ[var] = new_env[var]

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

    # set required env variables
    curr_dir = os.getcwd()
    os.chdir("/zipr/")
    set_env("./set_env_vars")
    os.chdir("/zafl/")
    set_env("./set_env_vars")
    os.chdir(curr_dir)

    # instrument and replace target 
    cmd = f'zafl.sh {target_binary_path} {target_binary_path}.zafl'

    print(f'Adding instrumentation (running command: {cmd}) ...')
    os.system(cmd)

    if os.path.isfile(f'{target_binary_path}.zafl'):
        os.system(f'cp {target_binary_path}.zafl {target_binary_path}')
    else:
        print('zafl transform failed!')
        exit(1)


def fuzz(input_corpus, output_corpus, target_binary):
    ''' run benchmark. '''
    aflplusplus_fuzzer.fuzz(input_corpus, output_corpus, target_binary)
