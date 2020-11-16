# Cati package manager
cati is a package manager for GNU/Linux/UNIX systems. cati is written in python

## Why cati?
some features of cati:

- cati is user friendly, very simple and easy to use
- cati has all in one, you don't need to have package manager, dependency manager and graphical interface splited, all of them is in one in cati
- cati repositories structure is simple and also smart and powerful
- cati packages format is `.cati`, also cati supports `.deb` and `.rpm` packages alongside `.cati` packages
- cati has a useful graphical interface

## Authors
cati writed by [parsampsh](https://github.com/parsampsh) and [contributors](https://github.com/parsampsh/cati/graphs/contributors)

## License
cati [licensed](/LICENSE) under GPL-v3

## Documentation
you can read full documentation of cati in [doc folder](/doc)

## Contributing
if you want to contribute to cati project, read [contributing guide](/CONTRIBUTING.md)

## Security policy
read cati security policy in [here](/SECURITY.md).

## Installation
before installation, you need to install `python3`, `pip3` and `virtualenv` on your system.
to check them, run this commands in terminal:

```bash
python3 --version
python3 -m pip --version
virtualenv --version
```

to compile and install cati on your system, do the following steps:

```bash
git clone https://github.com/parsampsh/cati.git
cd cati

# install dependencies
virtualenv venv -p python3
source venv/bin/activate
python3 -m pip install -r requirements.txt

# compile and install
make
sudo make install clean
```

now you can run cati in termianl:

```bash
cati
```
