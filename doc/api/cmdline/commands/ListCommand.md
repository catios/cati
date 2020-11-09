Module cmdline.commands.ListCommand
===================================
List command

Classes
-------

`ListCommand()`
:   List command

    ### Ancestors (in MRO)

    * cmdline.BaseCommand.BaseCommand

    ### Methods

    `config(self) ‑> dict`
    :   Define and config this command

    `help(self)`
    :   shows list of packages
        Options:
        --installed: show only installed packages
        --installed-manual: show only manual installed packages
        --author: filter packages list by author name. `--author='name of wanted author'` or more than 1 author: `--author='author 1 | author 2 | author 3'` (split with '|')
        --maintainer: filter packages list by maintainer name. `--maintainer='name of wanted maintainer'` or more than 1 author: `--maintainer='maintainer 1 | maintainer 2 | maintainer 3'` (split with '|')
        --category: filter packages list by category name. `--category='name of wanted category'` or more than 1 category: `--category='category 1 | category 2 | category 3'` (split with '|')
        --search: search by packages name and description `--search="someword"`

    `run(self)`
    :   Run command

    `show_once(self, package: package.Pkg.Pkg)`
    :   show once item in loaded packages list