#
# hash.py
#
# the cati project
# Copyright 2020 parsa mpsh <parsampsh@gmail.com>
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

""" Some helper functions for hashing """

import hashlib

def calc_file_sha256(filepath):
    """ gets filepath and calculates sha256 sum of that """
    sha256_hash = hashlib.sha256()
    f = open(filepath, 'rb')
    for byte_block in iter(lambda: f.read(4096),b""):
        sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def calc_file_sha512(filepath):
    """ gets filepath and calculates sha512 sum of that """
    sha512_hash = hashlib.sha512()
    f = open(filepath, 'rb')
    for byte_block in iter(lambda: f.read(4096),b""):
        sha512_hash.update(byte_block)
    return sha512_hash.hexdigest()

def calc_file_md5(filepath):
    """ gets filepath and calculates md5 sum of that """
    md5_hash = hashlib.md5()
    f = open(filepath, 'rb')
    for byte_block in iter(lambda: f.read(4096),b""):
        md5_hash.update(byte_block)
    return md5_hash.hexdigest()
