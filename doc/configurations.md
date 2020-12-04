# Cati Configurations
cati has some `Editable Text Configurations` (/etc/cati directory).
you can edit them with your editor.

### Allowed Architectures
cati checks package architecture while installing that. for example, cati does not installs `amd64` package on `i386` system. cati only installs packages with `all` and your system architecture. also you can add another allowed architectures. you can add them in `/etc/cati/allowed-architectures.list` file. as default, this file is empty.
but you can add another files like this syntax:

```
amd64
i386
...
```

you have to write archs line by line.
