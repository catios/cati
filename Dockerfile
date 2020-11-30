FROM python:3.9-buster

# copy source
COPY . /src
WORKDIR /src

# install requirements
RUN pip3 install -r requirements.txt

# compile and install
RUN make
RUN make install

# run cati
RUN cati

CMD ["bash"]
