# Security blacklist system
this feature helps to detect and block malware and bad packages.
this is a database contains list of malware packages with `sha256`, `sha512` and `md5` hash of them.
cati checks hash of package in this database in installation process. if package was detect in this database, cati shows error and detailed information in blacklist to user and cancels installation process.

### data structure
to set this list, you need to create json files in `/var/lib/cati/security-blacklist/`

for example, we create `/var/lib/cati/security-blacklist/part-1.json` and put this content:

```json
[
    {"title": "somemalware", "description": "hello world", "md5": "<md5>", "sha256": "<sha256>", "sha512": "<sha512>"},

    {"title": "somemalware", "description": "hello world", "md5": "<md5>", "sha256": "<sha256>", "sha512": "<sha512>"},

    {"title": "somemalware", "description": "hello world", "md5": "<md5>", "sha256": "<sha256>", "sha512": "<sha512>"},
]
```

replace `<md5>, <sha256>, <sha512>` with hash of bad package .cati file.
