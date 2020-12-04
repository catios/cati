Module repo.Repo
================
Cati repository model

Classes
-------

`Repo(config: str)`
:   Cati repository model

    ### Static methods

    `get_list() ‑> list`
    :   returns list of repositories
        
        Returns:
            list[Repo]: list of loaded repositories

    ### Methods

    `get_arch_str(self) ‑> str`
    :   Returns self.arch list (allowed package arch of repo) as string
        
        Returns:
            str

    `get_data(self, download_event=None) ‑> str`
    :   Recives repo data returns data as json
        
        Args:
            download_event (callable, None): if repo driver is http, this should be a function to download data
        
        Returns:
            str: repository data

    `get_pkg_str(self) ‑> str`
    :   Returns self.pkg list (allowed package type of repo) as string
        
        Returns:
            str

    `test(self) ‑> bool`
    :   Test repository
        
        Returns:
            bool: True means connection is ok, False means not