# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Integration code for AFLplusplus fuzzer."""

import os
import shutil
import subprocess

from fuzzers import utils
from fuzzers.aflplusplus import fuzzer as aflplusplus_fuzzer


def build():
    """Build benchmark."""
    build_directory = os.environ['OUT']

    # move fuzzer and qemu tracer to build directory
    shutil.copy('/afl/afl-fuzz', build_directory)
    shutil.copy('/afl/afl-qemu-trace', build_directory)

    # build benchmark
    os.environ['CC'] = 'clang'
    os.environ['CXX'] = 'clang++'
    os.environ['CFLAGS'] = ' '.join(utils.NO_SANITIZER_COMPAT_CFLAGS)
    cxxflags = [utils.LIBCPLUSPLUS_FLAG] + utils.NO_SANITIZER_COMPAT_CFLAGS
    os.environ['CXXFLAGS'] = ' '.join(cxxflags)
    os.environ['FUZZER_LIB'] = '/util/libAFLRewriteDriver.a'
    utils.build_benchmark()

def fuzz(input_corpus, output_corpus, target_binary):
    """Run fuzzer."""

    # Get LLVMFuzzerTestOneInput address.
    nm_proc = subprocess.run(
        [
            'sh', '-c',
            'nm \'' + target_binary + '\' | grep -i \'T afl_rewrite_driver_stdin_input\''
        ],
        stdout=subprocess.PIPE,
        check=True
    )

    target_func = '0x' + nm_proc.stdout.split()[0].decode('utf-8')
    print('[fuzz] afl_rewrite_driver_stdin_input() address =', target_func)

    # Fuzzer options for qemu_mode.
    flags = ['-Q']
    os.environ['AFL_QEMU_PERSISTENT_ADDR'] = target_func
    os.environ['AFL_ENTRYPOINT'] = target_func
    os.environ['AFL_QEMU_PERSISTENT_CNT'] = '1000000'
    os.environ['AFL_QEMU_DRIVER_NO_HOOK'] = '1'

    aflplusplus_fuzzer.fuzz(input_corpus,
                            output_corpus,
                            target_binary,
                            flags=flags)
