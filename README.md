# Cati package manager
cati is a package manager for GNU/Linux/UNIX systems. cati is written in python

```
               /\       /\            * * * * * * * * * * * * * *
               | |_____| |            * Meow.....! I am Cati!   *
              |  --   --  |       ....* I can manage your       *
             |  { { * } }  | ..../    * Packages!               *
              |           |           *                         *
     __________|         |            * * * * * * * * * * * * * *
    /                     |
   /                      |
__/_  __  _________  _   _|
    |_| |_|       |_| |_|
```

## Why cati?
some features of cati:

- Cati is user friendly, very simple and easy to use
- Cati has all in one. You don't need to have package manager, dependency manager and graphical interface separated
- Cati repositories structure is simple and also smart and powerful
- Cati packages format is `.cati`, also cati supports `.deb` and `.rpm` packages alongside `.cati` packages
- Cati has some tools to check your system health and keep that secure
- Cati has a graphical interface(comming soon...)

## Authors
cati written by [parsampsh](https://github.com/parsampsh) and [contributors](https://github.com/catios/cati/graphs/contributors)

## License
cati [licensed](/LICENSE) under GPL-v3

## Documentation
you can read full documentation of cati in [doc folder](/doc)

## Contributing
if you want to contribute to cati project, read [contributing guide](/CONTRIBUTING.md)

## Security policy
read cati security policy in [here](/SECURITY.md).

## Installation

### Installing via pip
You can install cati with pip:

```bash
sudo pip3 install cati
```

now you can run it:

```bash
cati
# OR
python3 -m cati
```

##### NOTE: surely run pip install using `sudo`

### Installing via Compiling the source code (Not recommended)

before compile and install cati, install the cati dev-dependencies:

- `python3 (>= 3.6)`
- `pip3`
- `virtualenv`
- `make`

to check them you can use the following commands:

```bash
python3 --version
python3 -m pip --version
virtualenv --version
make --version
```

then:

```bash
git clone https://github.com/catios/cati.git
cd cati

# install dependencies
virtualenv venv -p python3
source venv/bin/activate
python3 -m pip install -r requirements.txt

# compile and install
make -j4 # use `-jN` option to speed up build process
```

now, built execultable binary is created in `dist/cati`. you can run this by `./dist/cati`.

Also You can install this by running:

```bash
sudo make install clean
```

now you can run cati in termianl:

```bash
cati
```

If you want to remove it, use `make uninstall`:

```bash
sudo make uninstall
```

### Running without compiling
You can run Cati with python interpreter:

```bash
git clone https://github.com/catios/cati.git
cd cati

# install dependencies
virtualenv venv -p python3
source venv/bin/activate
python3 -m pip install -r requirements.txt

# run cati (argument `cati` points to `cati/` directory)
python3 cati
# OR
./cati/__main__.py
```
