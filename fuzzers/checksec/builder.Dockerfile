ARG parent_image
FROM $parent_image

# Install AFL requirements
RUN apt-get update && \
    apt-get install -y checksec

# Build driver
ADD ./util /util
RUN cd /util && make

# restore workdir
WORKDIR /src
