# Cati Package Manager Introduction
cati is a package manager for UNIX systems. cati can install/remove/list and manage packages on system. also cati can load packages lists from repositories(local file repositories and http server repositories). cati is very simple and easy to use and also is powerful.

## What is package manager?
An important part of GNU/Linux operation systems, is their package managers. Package manager is a program to manage installed programs on system. package manager can keep information of packages and list of them, remove/install/upgrade/downgrade packages and manage their dependnecy and conflicts and relations between packages.

The legacy package managers, are seprated in **Package manager**, **Dependency manager** and **Graphical interface**.
for example in Debian, we have `dpkg` as package manager, `apt` as dependnecy manager and `synaptic` as graphicla interface. But cati has all of them in one!

Package managers has some sections. in the cati, we have a **Repositories** section.

repositories are a place which package manager loads packages information from them. you can manage your repositories in cati and update information of packages from them. in this system, you can give a command to cati to install a package from repositories. cati fetches that package and installs that.

## Package archives
Packages are Files. an package, is packed and compressed as a file. cati packages format is `.cati`.
you can build, show and install that archives.

for example:

```bash
$ cati pkg show /path/to/firefox.cati
```

above command in terminal shows information of `firefox.cati` archive.

also cati has some commands to build packages.

also you can install them with `cati pkg install firefox.cati`.

also you can install packages from repositories:

```bash
# `install`, not `pkg install`
sudo cati install firefox
```

in this type of installation, cati downloads that `.cati` archive from repositores and installs that.

Cati keeps information of packages. cati knows which packages are installed, and which files is for that packages.
an important section of installing process, is copying package files on system.

for example, when you installing `firefox.cati`, file `/usr/bin/firefox` in this package will be copied on your system. then, when you enter `firefox` in your terminal, firefox will be open.

Package manager keeps list of installed files. when you removing a package, that package files will be removed:

```bash
sudo cati remove firefox # only `firefox`, not `firefox.cati`
```

You will learn more about cati usage in the next parts of documentation.
