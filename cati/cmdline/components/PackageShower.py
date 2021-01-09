#
# PackageShower.py
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

"""
Package shower cli component
"""

from cati.cmdline import ansi, pr
from cati.dotcati.Pkg import Pkg

def show(data: dict):
    """
    shows package information from data dictonary.
    
    Args:
        data: (dict) package data dictonary
    """
    output = ''
    output += 'Name: ' + ansi.green + data['name'] + ansi.reset + '\n'
    output += 'Version: ' + ansi.blue + data['version'] + ansi.reset + '\n'
    output += 'Arch: ' + ansi.yellow + data['arch'] + ansi.reset + '\n'
    try:
        author = data['author']
        output += 'Author: ' + ansi.header + author + ansi.reset + '\n'
    except:
        pass
    try:
        maintainer = data['maintainer']
        output += 'Maintainer: ' + ansi.cyan + maintainer + ansi.reset + '\n'
    except:
        pass
    try:
        changed_by = data['changed-by']
        output += 'Changed-By: ' + changed_by + '\n'
    except:
        pass
    try:
    	uploaders = data['uploaders']
    except:
    	uploaders = []
    if uploaders:
        output += 'Uploaders: '
        for uploader in uploaders:
            output += uploader + ', '
        output = output[:len(output)-2]
        output += '\n'
    try:
        channel = data['channel']
        output += 'Channel: ' + ansi.red + channel + ansi.reset + '\n'
    except:
        pass
    try:
        homepage = data['homepage']
        output += 'Homepage: ' + ansi.blue + homepage + ansi.reset + '\n'
    except:
        pass
    try:
        category = data['category']
        if category:
            output += 'Categories: '
            i = 0
            while i < len(category):
                output += ansi.bold + category[i] + ansi.reset
                if i < len(category)-1:
                    output += ', '
                i += 1
            output += '\n'
    except:
        pass
    try:
        description = data['description']
        output += 'Description: ' + description + '\n'
    except:
        pass
    try:
        changes = data['changes']
        output += 'Changes: ' + description + '\n'
    except:
        pass
    try:
        date = data['date']
        output += 'Last-Update-Date: ' + date + '\n'
    except:
        pass
    try:
        urgency = data['urgency']
        output += 'Update-Level: ' + urgency + '\n'
    except:
        pass
    try:
        essential = data['essential']
        if essential:
            essential = 'Yes'
        else:
            essential = 'No'
        output += 'Essential: ' + essential + '\n'
    except:
        pass
    try:
        file_size = Pkg.get_download_size_str(data['file_size'])
        output += 'Download-Size: ' + str(file_size) + '\n'
    except:
        pass
    try:
        installed_size = Pkg.get_download_size_str(data['installed-size'])
        output += 'Installed-Size: ' + str(installed_size) + '\n'
    except:
        pass
    try:
        repo = data['repo']
        output += 'Repository: ' + repo + '\n'
    except:
        pass
    try:
    	depends = data['depends']
    except:
    	depends = []
    if depends:
        output += 'Depends: '
        for dep in depends:
            output += ansi.bold + dep + ansi.reset + ', '
        output = output[:len(output)-2]
        output += '\n'
    try:
    	recommends = data['recommends']
    except:
    	recommends = []
    if recommends:
        output += 'Recommends: '
        for rec in recommends:
            output += ansi.bold + rec + ansi.reset + ', '
        output = output[:len(output)-2]
        output += '\n'
    try:
    	conflicts = data['conflicts']
    except:
    	conflicts = []
    if conflicts:
        output += 'Conflicts: '
        for conflict in conflicts:
            output += ansi.bold + conflict + ansi.reset + ', '
        output = output[:len(output)-2]
        output += '\n'
    try:
    	suggests = data['suggests']
    except:
    	suggests = []
    if suggests:
        output += 'Suggests: '
        for suggest in suggests:
            output += ansi.bold + suggest + ansi.reset + ', '
        output = output[:len(output)-2]
        output += '\n'
    try:
    	enhances = data['enhances']
    except:
    	enhances = []
    if enhances:
        output += 'Enhances: '
        for enhance in enhances:
            output += ansi.bold + enhance + ansi.reset + ', '
        output = output[:len(output)-2]
        output += '\n'
    try:
    	provides = data['provides']
    except:
    	provides = []
    if provides:
        output += 'Provides: '
        for provide in provides:
            output += ansi.bold + provide + ansi.reset + ', '
        output = output[:len(output)-2]
        output += '\n'
    if Pkg.is_installed(data['name']):
        installed_version = Pkg.installed_version(data['name'])
        if Pkg.is_installed_manual(data['name']):
            output += 'Installed-Manual: ' + installed_version + '\n'
        else:
            output += 'Installed: ' + installed_version + '\n'

    # show user defined fields
    for k in data:
        if k[0] == 'x' or k[0] == 'X':
            # that fields start with `x` character are user defined fields
            output += '\n' + k + ': ' + data[k]

    if output[-1] == '\n':
        output = output[:len(output)-1]
    pr.p(output.strip())
