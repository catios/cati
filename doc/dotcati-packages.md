# Dotcati packages (.cati)
extension of cati package manager package files is `.cati`. this files are `tar.gz` files.

structure of packages:

```
data.json
files/
    // package files...
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

    "category": ["list", "of", "categories"],
    "depends": [
        "pkga",
        "pkga >= 1.7.13",
        "pkgb | pkgc <= 1.0",
        "pkg1 = 1.0"
        "..."
    ],
    "conflicts": [
        "pkga",
        "pkga >= 1.7.13",
        "pkgb | pkgc <= 1.0",
        "pkg1 = 1.0"
        "..."
    ]
}
```

`depends` list making dependency to another packages. if that depended packages ARE NOT installed, this package will not install and cati shows error.

`conflicts` list making conflict to another packages. if that conflicted packages ARE installed, this package will not install and cati shows error.

## Building packages

to build `.cati` package, you should do the following steps:
- create a directory
- create `data.json` in that
- create `files/` folder in that
- write package information and configs in `data.json` as json format
- put package files to `files/` folder

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
