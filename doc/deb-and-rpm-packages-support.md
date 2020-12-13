# Deb and RPM packages support
cati has an useful feature, that is supporting `.deb` and `.rpm` packages.
actually, cati considers deb and rpm packages as `.cati` packages.

this system, converts `deb` and `rpm` packages to `cati` packages REAL TIME. means if you run this command:

```bash
cati pkg show some-deb-package.deb
```

cati converts `some-deb-package.deb` to an `.cati` package temporaily, and considers the `.cati` generated file.
