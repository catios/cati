FROM python:3.8-buster

# copy source
COPY . /src
WORKDIR /src

# install requirements
RUN cat requirements.txt | grep -v 'pkg-resources==0.0.0' > tmp-requirements.txt
RUN pip3 install -r tmp-requirements.txt

# compile and install
RUN make all
RUN make
RUN make install

# run cati
RUN cati

CMD ["bash"]
