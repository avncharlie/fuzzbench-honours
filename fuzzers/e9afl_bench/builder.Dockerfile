ARG parent_image
FROM $parent_image

# Install the necessary packages.
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        git \
        flex \
        bison \
        libglib2.0-dev \
        libpixman-1-dev \
        python3.9

# Download afl++
RUN git clone https://github.com/AFLplusplus/AFLplusplus.git /afl 

# Set default shared memory area size to be 65536 as otherwise e9afl crashes
RUN sed -i 's/^#define DEFAULT_SHMEM_SIZE .*/#define DEFAULT_SHMEM_SIZE 65536/' /afl/include/config.h
 
# Build afl++ without Python support as we don't need it.
# Set AFL_NO_X86 to skip flaky tests.
RUN cd /afl && \
    unset CFLAGS CXXFLAGS && \
    AFL_NO_X86=1 CC=clang PYTHON_INCLUDE=/ make

# Download and build e9afl
RUN apt-get install -y xxd
RUN git clone https://github.com/GJDuck/e9afl.git /e9afl
RUN cd /e9afl && ./build.sh

# Build driver
ADD ./util /util
RUN cd /util && make
