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
        
        Usage:
        - cati list [options]
        
        Options:
        --installed: show only installed packages
        --installed-manual: show only manual installed packages
        --author=[author-name or author-nameS splited by `|`]: filter packages list by author name
        --maintainer=[maintainer-name or author-nameS splited by `|`]: filter packages list by maintainer name
        --category=[category-name or category-nameS splited by `|`]: filter packages list by category
        --search=[word]: search by packages name and description

    `run(self)`
    :   Run command

    `show_once(self, package: package.Pkg.Pkg)`
    :   show once item in loaded packages list