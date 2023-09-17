ARG parent_image

FROM grammatech/ddisasm AS ddisasm 

FROM $parent_image

# Install ddisasm and gtirb-pprinter from prebuilt container
COPY --from=ddisasm /lib/x86_64-linux-gnu/libboost_filesystem.so.1.71.0 /lib/x86_64-linux-gnu/libboost_filesystem.so.1.71.0
COPY --from=ddisasm /lib/x86_64-linux-gnu/libboost_program_options.so.1.71.0 /lib/x86_64-linux-gnu/libboost_program_options.so.1.71.0
COPY --from=ddisasm /lib/libcapstone.so.5 /lib/libcapstone.so.5
COPY --from=ddisasm /lib/x86_64-linux-gnu/libgomp.so* /lib/x86_64-linux-gnu/
COPY --from=ddisasm /usr/local/lib/libgtirb.so* /usr/local/lib/
COPY --from=ddisasm /usr/local/lib/libgtirb_layout.so* /usr/local/lib/
COPY --from=ddisasm /usr/local/lib/libgtirb_pprinter.so* /usr/local/lib/
COPY --from=ddisasm /lib/x86_64-linux-gnu/libprotobuf.so* /lib/x86_64-linux-gnu/
COPY --from=ddisasm /usr/local/bin/ddisasm /usr/local/bin/
COPY --from=ddisasm /usr/local/bin/gtirb* /usr/local/bin/
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib"
ENV DEBIAN_FRONTEND=noninteractive 

# Install the necessary packages.
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        git \
        flex \
        bison \
        libglib2.0-dev \
        libpixman-1-dev \
        python3.9 \
        python3-pip

# Install gtirb rewriting
RUN python3.9 -m pip install gtirb gtirb-rewriting

# Download afl++
RUN git clone https://github.com/AFLplusplus/AFLplusplus.git /afl 
 
# Build afl++ without Python support as we don't need it.
# Set AFL_NO_X86 to skip flaky tests.
RUN cd /afl && \
    unset CFLAGS CXXFLAGS && \
    AFL_NO_X86=1 CC=clang PYTHON_INCLUDE=/ make

# Download afl-rewrite
RUN mkdir /root/.ssh/
RUN echo -e "\e[93mTo build, copy your private ssh key (~/.ssh/id_rsa) into to the build directory (fuzzbench/fuzzers/afl_rewrite/)\n\
This is to clone the private afl-rewrite git repo.\n\
\e[91mTHIS IS PROBABLY NOT SECURE. Run at your own risk!\e[0m"
ADD id_rsa /root/.ssh/id_rsa

RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

RUN git clone -b fuzzbench git@github.com:avncharlie/afl-rewrite.git /afl-rewrite

# Build driver
RUN cd /afl-rewrite/util && make 
