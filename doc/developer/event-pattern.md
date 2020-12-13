# Event pattern

source code of cati has a pattren named `event pattern`. this pattern created to full split cli/gui layer and program core layer.

in this pattern, we never print any thing from core of program. this pattern says all of cli interactions need to be in cli layer. for example, in the core of program, some operations are running and program need to print something between that operaions, for example:

```
installing package somepkg1 (1.0)... OK
installing package somepkg2 (1.0)... OK
```

this prints in cli, are not from core of installer. this is from cli layer. but this actions passed to installer core and installer core call them.

for example:

```python
# NOTE: the following code is just a example and is not part of real code
# ...

def installing_package_event(pkg):
    pr.p('instaalling ' + pkg.data['name'])

def package_installed_event(pkg):
    pr.p('OK')

Installer.install(pkg, event: {
    'installing_package': installing_package_event,
    'package_installed': package_installed_event
})

# ...
```

for example now, in the above code, installer calls that passed functions as `event`.

the event pattern is very important and is used in all of code.
in core functions, events are documented in function docstring.
