FROM gcr.io/fuzzbench/base-image

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y upgrade && apt-get -y install \
        build-essential \
        gcc \
        g++ \
        make \
        cmake \
        git \
        gdb \
        ca-certificates \
        tar \
        gzip \
        vim \
        joe \
        wget \
        curl \
        apt-utils \
        libiberty-dev \
        libboost-all-dev \
        libdw-dev \
        libtbb2 \
        libtbb-dev \
        build-essential         \
        cmake                   \
        libboost-atomic-dev     \
        libboost-chrono-dev     \
        libboost-date-time-dev  \
        libboost-filesystem-dev \
        libboost-thread-dev     \
        libboost-timer-dev      \
        libtbb-dev              \
        gettext                 \
        bzip2                   \
        zlib1g-dev              \
        m4                      \
        libiberty-dev           \
        pkg-config              \
        clang                   \
        libomp-dev \
        checkinstall \
    && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

# install elfutils, dyninst and afl dyninst
ADD elfutils_1-1_amd64.deb elfutils_1-1_amd64.deb
RUN dpkg -i elfutils_1-1_amd64.deb

ADD dyninst_build_20231015-1_amd64.deb dyninst_build_20231015-1_amd64.deb
RUN dpkg -i dyninst_build_20231015-1_amd64.deb

ADD afl-dyninst_1-1_amd64.deb afl-dyninst_1-1_amd64.deb
RUN dpkg -i afl-dyninst_1-1_amd64.deb

# setup afl-dyninst
RUN echo "/usr/local/lib" > /etc/ld.so.conf.d/dyninst.conf && ldconfig
ENV DYNINSTAPI_RT_LIB=/usr/local/lib/libdyninstAPI_RT.so
