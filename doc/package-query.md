# Package query

package query is a string to check package(s) installation status. this queries are used in dependency and conflicts declaring system in packages.

look at this example: `pkg1 > 4.0`

above example checks an package named `pkg1` is installed and installed version is upper than `4.0`.

to test this queries, you can check them with `cati query` command:

```bash
cati query "pkg1 > 4.0"
```

so, now you know base structure of query strings. lets go to learn more.

### only checking package installation
in this type, you just want to an package be installed. (means installed version is not important).

to check this type of query, you just need to write name of package without anything else.

example: `pkg1`

### `>` operation
this operation, checks that installed version is upper than specify version.

example: `pkg1 > 3.6`

in this type of query, you should write name of package and an space, and next write `>` character with an space and next write that version you want

### `<` operation
this operation is like `>` but reverse. you can check installed version is less than an specify version.

example: `pkg1 < 5.0`

### `>=` and '<='
this operations are like `>` and `<` but they are not `less` or `upper`, they are `less or equals` and `upper or equals`.

for example if `pkg1` installed version is `3.2` and you check query `pkg1 > 3.2`, you will get `False` result. but if you write `pkg1 >= 3.2` you will get True result.

### `=` operation
this operation just checks one specify version.

example: `pkg1 = 7.4`

result of above query will be True if pkg1 installed version is `7.4`, not anything else.

### `|` (or) operation
you can check more than 1 query, in 1 query :).

for example, your package wants a webserver, `nginx` OR `apache2`. so, you don't requirung both of them, you also are ok with one of them. so you want to say i want `nginx` or `apache2` or both of them (means one of them is enough but if all of them also are installed, i don't have problem).

the query: `nginx | apache2`

also you can use all of `>,<,=,>=,<=` operations in this type of query.

for example: `pkg1 >= 3.0 | pkg2 = 1.0 | pkg3`

### `&` operation
this operation is like `|`, but this is `AND`, not `OR`.

you want (`nginx`) or (`apache2` and `php7.4`). how to write this query? yes. we use `&` operation.

example: `nginx | apache2 & php7.4`

another example: `pkg1 >= 6.5 | pkg2 & pkg3 > 1.0`

### file query
also you can use file dependency/conflict. you have to write `@/path/to/file`. for example if you set this as a dependency, that file should be exists for this package, and if you set this as a conflict, package will not install if that file/dir exists. also you can check file sha256. for example `@76883f0fd14015c93296f0e4202241f4eb3a23189dbc17990a197477f1dc441a@/path/to/file`. you should write an `@` and next write specify sha256 and next again an `@` and next file path. now that file should exists, also cati checks sha256 of that file and compares that with your specify hash.

also you can use this feature in all of previous features.

for example: `pkg1 > 5 | @/usr/bin/pkg1 & pkg2`
another example: `pkga <= 7 | @/usr/bin/pkg1 & pkg2 | @76883f0fd14015c93296f0e4202241f4eb3a23189dbc17990a197477f1dc441a@/path/to/file`
