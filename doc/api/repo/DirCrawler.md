Module repo.DirCrawler
======================
Crawls an directory and extracts packages data from that

Classes
-------

`DirCrawler(dirpath: str)`
:   Crawls an directory and extracts packages data from that

    ### Methods

    `add_once(self, path: str)`
    :   add once package data item
        
        Args:
            path (str): package filepath

    `start(self, path='')`
    :   start crwaling (loaded packages will put in self.loaded_packages)
        
        Args:
            path (str): directory path