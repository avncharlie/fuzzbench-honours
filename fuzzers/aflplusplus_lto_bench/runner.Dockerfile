FROM gcr.io/fuzzbench/base-image

RUN apt-get update && \
    apt-get -y install --no-install-suggests --no-install-recommends \
    git \
    wget \
    apt-utils apt-transport-https ca-certificates gnupg dialog

RUN echo "deb http://apt.llvm.org/focal/ llvm-toolchain-focal-13 main" >> /etc/apt/sources.list && \
    wget -qO - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -

RUN echo "deb http://ppa.launchpad.net/ubuntu-toolchain-r/test/ubuntu focal main" >> /etc/apt/sources.list && \
    apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 1E9377A2BA9EF27F

RUN apt-get update && apt-get full-upgrade -y && \
    apt-get -y install --no-install-suggests --no-install-recommends \
    clang-13 clang-tools-13 libc++1-13 libc++-13-dev \
    libc++abi1-13 libc++abi-13-dev libclang1-13 libclang-13-dev \
    libclang-common-13-dev libclang-cpp13 libclang-cpp13-dev liblld-13 \
    liblld-13-dev liblldb-13 liblldb-13-dev libllvm13 libomp-13-dev \
    libomp5-13 lld-13 lldb-13 llvm-13 llvm-13-dev llvm-13-runtime llvm-13-tools
