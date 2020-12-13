# Version channels
dotcati packages has a property named `channel`.
this field is for making category for versions.

this is an example version list:

```
1.0-dev
1.0-dev1
1.0-dev2
1.0-alpha
1.0-alpha1
1.0-beta0
1.0-beta2
1.0-beta3
1.0-rc0
1.0-rc1
1.1-alpha
1.1-rc0
1.1
...
```

this versions are different. the `alpha` and `beta` versions are not stable releases. normal users don't want to install beta or alpha versions. Package maintainer should split this versions. but how?

look at this list (`<version> -> <channel>`):

```
1.0-dev -> dev
1.0-dev1 -> dev
1.0-dev2 -> dev
1.0-alpha -> alpha
1.0-alpha1 -> alpha
1.0-beta0 -> beta
1.0-beta2 -> beta
1.0-beta3 -> beta
1.0-rc0 -> release
1.0-rc1 -> release
1.1-alpha -> alpha
1.1-rc0 -> release
1.1 -> release
```

now, we have 4 channels: `dev`, `alpha`, `beta` and `release`.

if user don't want to get update for `dev`, `alpha` and `beta` verisons, can set `channel` field for repositoriess:

```
https://pkg.example.com/packages name=main arch=all,amd64 pkg=cati channel=release
```

the `channel` option for repository, tells to cati to only recive versions in `release` channel.
then, if user update repos data, versions list of package is this:

```
1.0-rc0 -> release
1.0-rc1 -> release
1.1-rc0 -> release
1.1 -> release
```

`dev`, `alpha` and `beta` channels are ignored.

the release names (for example here `dev`, `alpha`...) has not a specify standard. you can set any channel name for versions, but users should be sync with them in repository lists.

also users can set multiple channels:

```
https://pkg.example.com/packages name=main arch=all,amd64 pkg=cati channel=release,beta
```

in above example, `release` and `beta` channels are loaded:

```
1.0-beta0 -> beta
1.0-beta2 -> beta
1.0-beta3 -> beta
1.0-rc0 -> release
1.0-rc1 -> release
1.1-rc0 -> release
1.1 -> release
```
