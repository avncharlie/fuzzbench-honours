FROM grammatech/ddisasm AS ddisasm 

FROM gcr.io/fuzzbench/base-image
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

# Install gtirb rewriting
RUN apt-get update && apt-get install -y python3.9 python3-pip
RUN python3.9 -m pip install gtirb gtirb-rewriting
