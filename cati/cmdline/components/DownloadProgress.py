#
# DownloadProgress.py
#
# the cati project
# Copyright 2020-2021 parsa shahmaleki <parsampsh@gmail.com>
#
# This file is part of cati.
#
# cati is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cati is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cati.  If not, see <https://www.gnu.org/licenses/>.
##################################################

""" Cli download progress bar """

import wget

def download(url: str, output_path=None) -> (bool, Exception):
    """
    Download `url` and save in `output_path` and shows progress in terminal

    Args:
        url: (str) that url you want to download
        output_path: (str) that path you want to download file in that (optional)

    Returns:
        bool True: means download is successful
        instance of Exception: means download faild and returns exception
    """
    try:
        wget.download(url, out=output_path)
        print()
        return True
    except Exception as ex:
        return ex
