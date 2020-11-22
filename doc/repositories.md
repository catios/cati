# Cati Repositories
repository is an server/directory that hosting packages.

normaly, you don't install packages manually and locally. you can add repositories to your cati and cati automatic loads packages list from that repository and also you can install packages from that repositories.

we have two types of repository: `Local:File` and `Server:Http`.

in local type, packages are in a directory and cati loads list of packages from that directory. in type server, packages hosted in an server and cati downloads list of packages from that server.

## manage/update repos
you can manage repositories with `cati repo` command:

```bash
cati repo # show list of repositories
cati --add '<new repo>' # add new repository
cati --edit # open cati repositories config file with editor
```

cati repositories are configed in `/etc/cati/repos.list` file. 
also you can add seprated files in `/etc/cati/repos.list.d/` directory.

example of `/etc/cati/repos.list`:

```
https://cati.example.com/packages pkg=cati arch=i386 name=example-repo
https://cati.example.com/packages pkg=cati arch=all name=example-repo2
https://cati.example.com/packages pkg=deb arch=all name=example-repo3
file:///path/to/packages pkg=cati arch=all name=local-repo
```

also we create an file in `/etc/cati/repos.list.d/another-repo`:

```
https://cati.example.com/path/to/another/repo pkg=cati arch=i386 name=another-repo
```

now, we run:

```bash
cati repo
```

and we can see list of configured `5` repos.

now, for updating packages list from configured repositories, we have to use `cati update` command:

```bash
sudo cati update
```

### Repositories config options
look at this example of `/etc/cati/repos.list`:

```
http://pkg.example.com/packages pkg=cati name=example-repo arch=amd64 priority=10
```

What is that `pkg=cati`, `name=example-repo` and...?

they are repo config options.

`pkg=<package-type>` says to cati to load what type of packages from the repository. default type is `cati`.

`arch=<architecture>` says to cati to load packages with which architecture from that repo. default arch is architecture of your system.

`name=<name>` just sets an name for repository. default name is `main`.

`priority=<number>` sets priority of the repo between another repos. for example if we have 2 repos and package firefox version 83 is in both of them, cati consider which of them as `firefox=83`? package of that repo with much priority will consider as `firefox=83`. priority number is reverse. for example priority `2` is upper than `10`. default priority is `1`.

so, with this options we have this strcuture:

```
<repo-address> name=<name> arch=<arch> priority=<priority>  pkg=<pkg-type>
```

also you can don't set all of that options and just write address of repo. cati uses default values for them.

also, repo address should be started with `file://` or `http://` or `https://`.

## Local repository
look at this example for local repository. for example, this is an directory tree:

```
/local-repo/
           /packages/
                    /f/
                      /firefox/
                              /firefox-80-amd64.cati
                              /firefox-83-i386.cati
                    /p/
                      /php/
                          /php-7.4-i386.cati
```

cati can load packages list from this directory. first, this directory should be scaned:

```bash
cati repo --scan /path/to/local-repo
```

now, to add this repository, you can run this command:

```bash
sudo cati repo --add 'file:///path/to/local-repo/packages pkg=cati arch=i386 name=test-repo'
```

next, to update list of packages from repos run:

```bash
sudo cati update
```

now, if you get list of packages by running:

```bash
cati list
```

you will see `firefox` and `php`.

also you can set an subpath from repo as repository. look at this example:

```
file:///path/to/local-repo/packages/f/firefox pkg=cati arch=i386 name=test-repo
```

in this example, after update just `firefox` is loaded. actually we can set an subpath and cati just loads content of that path.

## Http repositories
look at this example about cati server repositories.

for example, `http://pkg.example.com` is an cati repository.

we can add this to our repos:

```bash
sudo cati repo --add 'http://pkg.example.com/packages pkg=cati arch=amd64 name=my-repo'
```

next, we update lists:

```bash
sudo cati update
```

now, list of packages in that server is loaded in our local database packages list.

also like local repos, you can set an subpath for repo. for example:

```
http://pkg.example.com/packages/f/firefox pkg=cati arch=amd64 name=my-repo
```

## Building cati repository server
building and maintaining cati repositories is very simple and easy.

first, you have to install `cati` and `php` on your server.

next, create an directory and put packages in that.

next, scan that directory:

```bash
cati repo --scan /path/to/dir
```

next, copy cati repository php script [`repository/server.php`](/repository/server.php) in that directory.

next, go to your directory and run this command to serve that for test:

```bash
cd /path/ti/directory
php -S localhost:8000 server.php
```

now, go to http://localhost:8000. you can see your repo.

now, you cannot use `php -S localhost:8000 server.php` command in production. you have to install an webserver and config your webserver to serve that repo directory and redirect all of requests to `server.php`.

Enjoy it!
