ARG parent_image

# Download and build zipr in its own image (doesn't work in base image)
FROM ubuntu:focal as zipr_builder
RUN apt-get update
RUN apt-get install -y lsb-release sudo git
RUN git clone --recurse-submodules https://git.zephyr-software.com/opensrc/zipr.git /zipr
WORKDIR /zipr
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
RUN ./get-peasoup-packages.sh all
RUN bash -c "source ./set_env_vars && scons"

FROM $parent_image

# Install AFL requirements
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        git \
        flex \
        bison \
        libglib2.0-dev \
        libpixman-1-dev \
        python3
# Download afl++
RUN git clone https://github.com/AFLplusplus/AFLplusplus.git /afl 
# Build afl++ without Python support as we don't need it.
# Set AFL_NO_X86 to skip flaky tests.
RUN cd /afl && \
    unset CFLAGS CXXFLAGS && \
    AFL_NO_X86=1 CC=clang PYTHON_INCLUDE=/ make

# Copy zipr
COPY --from=zipr_builder /zipr /zipr
# install needed packages in builder image and setup zipr database
RUN apt-get install -y lsb-release sudo
RUN bash -c "cd /zipr && ./get-peasoup-packages.sh all"
ENV USER=root
RUN bash -c "cd /zipr && service postgresql start && ./postgres_setup.sh"

# Download and build zafl 
RUN git clone --recurse-submodules https://git.zephyr-software.com/opensrc/zafl.git /zafl
RUN apt-get install -y clang fakeroot dpkg
RUN bash -c "cd /zipr && source ./set_env_vars && cd /zafl && source ./set_env_vars && scons"

# Build driver
ADD ./util /util
RUN cd /util && make
