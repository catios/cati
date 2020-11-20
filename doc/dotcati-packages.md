# Dotcati packages (.cati)
extension of cati package manager package files is `.cati`. this files are `tar.gz` files.

structure of packages:

```
data.json
files/
    // package files...
scripts/
    // package scripts...
```

`data.json` is main file of a package. this file contains information of package.
an example for this file:

```json
{
    "name": "nameofpackage(required)",
    "version": "version.of.package(required)",
    "arch": "architecture-of-package(required, `all` arch means this package is for all of architectures)",

    "__comment__": "the following fields are optional",

    "author": "the main developer of program",
    "maintainer": "maintainer of this package",
    "description": "description of this package",
    "channel": "channel of this version",
    "homepage": "homepage url",
    "category": ["list", "of", "categories"],

    "depends": [
        "pkga",
        "pkga >= 1.7.13",
        "pkgb | pkgc <= 1.0",
        "pkg1 = 1.0",
        "pkg1 >= 2.0 | @/path/to/some/file",
        "@/another/file | @/thefile",
        "@76883f0fd14015c93296f0e4202241f4eb3a23189dbc17990a197477f1dc441a@/path/to/file",
        "..."
    ],
    "conflicts": [
        "pkga",
        "pkga >= 1.7.13",
        "pkgb | pkgc <= 1.0",
        "pkg1 = 1.0",
        "@/i/have/conflict/with/this/file",
        "@76883f0fd14015c93296f0e4202241f4eb3a23189dbc17990a197477f1dc441a@/path/to/file",
        "..."
    ],
    "suggests": [
        "another-pkg",
        "pkg2",
        "..."
    ],

    "conffiles": [
        "/path/to/some/file",
        "/path/to/some/dir",
        "/etc/somefile"
        "..."
    ],

    "staticfiles": [
        "/path/to/some/static/file",
        "/usr/bin/somefile",
        "..."
    ]
}
```

`depends` list making dependency to another packages. if that depended packages ARE NOT installed, this package will not install and cati shows error.

`conflicts` list making conflict to another packages. if that conflicted packages ARE installed, this package will not install and cati shows error.

also you can use file depend/conflict in `depends` and `conflicts` lists. you have to write `@/path/to/file`. for example if you set this as a dependency, that file should be exists for this package, and if you set this as a conflict, package will not install if that file/dir exists. also you can check file sha256. for example `@76883f0fd14015c93296f0e4202241f4eb3a23189dbc17990a197477f1dc441a@/path/to/file`. you should write an `@` and next write specify sha256 and next again an `@` and next file path. now that file should exists, also cati checks sha256 of that file and compares that with your specify hash.

`suggests` field declares an list from related packages to this package. you have to just list name of related packages.

`conffiles` list declares a list from file/dir paths to set them as config file. config files will not remove in remove process (user can remove them with `--conffiles` in remove command). if some files in your package keeps configuration and something like that, add path of that file to this list

`staticfiles` list declares a list from files where should be static and not changed. for example, binary files are static but configuration files maybe change. this system helps to keep system secure. cati can check static files and if cati detect some changes in that files, gives warning to user and can repair that package by re-installing that.

to know about `depends` and `conflicts` lists items query syntax, read [Package query](/doc/package-query.md).

### scripts
there is an directory named `scripts` in package build directory.

you can write some scripts for packages.

scripts:
- `ins-before`: will run before start installation process
- `ins-after`: will run after installation process
- `rm-before`: will run before remove process
- `rm-after`: will run after remove process
- `any`: any script will run after ANY install/remove process for any package

for example, you can create a file named `ins-before` in `scripts` folder (`scripts/ins-before`) and write an shell script in that.

if an script returns an non-zero code, the process will be stoped (only for installation scripts).

#### more about `any` script
when you installing a package where has a `any` script, this script will save in system and will run after any install or remove process on any package. this script is a general script and will run after all of transaction.

you may see something like this in terminal while installing/removing packages:

```
Processing scripts for pkg1...
Processing scripts for pkg2...
...
```

this message means cati are running `any` script of package `pkg1`, `pkg2`...

#### scripts arguments
package scripts maybe get some arguments. this arguments maybe useful for your script.

Arguments of scripts:

- `ins-before` and `ins-after`: this scripts get old version of package. if package is not installed already and this is new install, them don't get any argument. for example, if package version `1.0` installed and user is installing version `1.2`, you script will get argument `1.2`.
- `rm-before` and `rm-after`: this scripts will get an argument with two types: `with-conffiles` or `without-conffiles` this means remove process is with config files or not.
- `any`: any script gets list of processed transactions. this is two types; `remove` or `install`. if runed processes are installation processes, arguments are like this: `install <pkg-name>@<version> <pkg-name>@<version> <pkg-name>@<version> ...` and if processes are remove, arguments are like this: `remove <pkg-name>@<version> <pkg-name>@<version> <pkg-name>@<version> ...`. this maybe useful for your script.

## Building packages

to build `.cati` package, you should do the following steps:
- create a directory
- create `data.json` in that
- create `files/` folder in that
- write package information and configs in `data.json` as json format
- put package files to `files/` folder
- create `scripts/` folder and create package scripts in that (optional)

next build package with this command:

```bash
cati pkg build your-package/
```

package is created in `your-package.cati`.

if you want specify a path for package output, use `--output` or `-o` option:

```bash
cati pkg build your-package/ --output='thepackage.cati'
# or
cati pkg build your-package/ -o='thepackage.cati'
```

now, to show your package:

```bash
cati pkg show your-package.cati # or path to your package file
```

#### `files` directory structure

all of files and dirs in `files/` folder of your package, will be copy on system.

for example:

```
files/
    usr/
        bin/
            myapp
    etc/
        myapp/
            some-file.txt
```
