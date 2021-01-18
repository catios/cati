# Distribution Guide

If you want to create a GNU/Linux distribution with Cati package manager, this guide is helpful for you.

---

Actually, all of GNU/Linux distros have some packages to be installed by default. that packages are in the installer.
for cati, this is so easy. you have to put your packages (`.cati` or something else) in a folder in your installer with any directory structure you want.
for example in `packages/` folder. then, in installtion process, your installer should copy that folder to installation partition(cati should be installed on the partition before this process). then your installer does chroot to that partition. then the following commands on cati should be runed by installer(in chroot state):

```bash
cati repo --scan /path/to/copied/packages/dir
cati repo --add 'file:///path/to/copied/packages/dir arch=all,<the-installer-arch> pkg=cati(or anything else) priority=1 name=installer-packages'
cati update
```

for example:

```
cati repo --scan /path/to/copied/packages/dir
cati repo --add 'file:///path/to/copied/packages/dir arch=all,amd64 pkg=cati priority=1 name=installer-packages'
cati update
```

then, your installer can run cati install commands to install all of needed packages:

```bash
cati install pkg1 pkg2 pkg3 ...
```

after installing packages from pool, your installer needs to remove copied packages directory on installation partition:

```bash
rm -rf /path/to/copied/packages/dir # or every other ways to delete that
```

next, you have to remove temporaily seted repo and set your distro repositories:

```
rm /etc/cati/repos.list.d/*
echo '' > /etc/cati/repos.list

# set your distro repos
echo '<my-repo>' > /etc/cati/repos.list
# OR
cp /path/to/installer/cdrom/repos.list /etc/cati/repos.list # or copy from anything else
```

then, you can optionally update repos(if user wants to get updates):

```bash
cati update
```

also you can recive all of upgrades(if user wants to recive upgrades):

```bash
cati upgrade -y
```

also that is recommended to run this command to finally check in the end of installation process:

```bash
cati check
```

If above command returned non-zero code, you installer can try `--autofix` option to fix some problems automatic
(This action needs to get back repository, so we recommend don't delete installer repo before this step and delete them after this):

```bash
cati check --autofix
```
