Module cmdline.components.DownloadProgress
==========================================
Cli download progress bar

Functions
---------

    
`download(url: str, output_path=None) ‑> (<class 'bool'>, <class 'Exception'>)`
:   Download `url` and save in `output_path` and shows progress in terminal
    
    Args:
        url: (str) that url you want to download
        output_path: (str) that path you want to download file in that (optional)
    
    Returns:
        bool True: means download is successful
        instance of Exception: means download faild and returns exception