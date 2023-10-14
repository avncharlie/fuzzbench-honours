ARG parent_image
FROM $parent_image

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python3-dev \
        python3-setuptools \
        automake \
        cmake \
        git \
        flex \
        bison \
        libglib2.0-dev \
        libpixman-1-dev \
        cargo \
        libgtk-3-dev \
        gcc-9-plugin-dev
# hardcoded gcc version is probably going to break
# used to build gcc mode

# Download afl++
RUN git clone https://github.com/AFLplusplus/AFLplusplus.git /afl 
 
# Build afl++ without Python support as we don't need it.
# Set AFL_NO_X86 to skip flaky tests.
RUN cd /afl && \
    unset CFLAGS CXXFLAGS && \
    AFL_NO_X86=1 CC=clang PYTHON_INCLUDE=/ make

# Build driver
ADD ./util /util
RUN cd /util && make
