FROM almalinux:9
SHELL [ "/bin/bash", "-c"]
RUN dnf install -y git procps

# get externals
RUN mkdir /b2-ext
RUN git clone https://github.com/belle2/externals.git /b2-ext-repo

# get necessary tools for installation
RUN git clone https://github.com/belle2/tools.git /b2-tools
RUN git config --global --add safe.directory /b2-tools
RUN source /b2-tools/b2setup &&\
./b2-tools/b2install-prepare --non-interactive
RUN rm -r b2-tools

RUN dnf clean all
COPY ./script /script