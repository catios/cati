#
# PkgConvertor.py
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

""" Deb and Rpm to cati package convertor """

import os
import sys
import shutil
import json
from frontend import Temp
from cmdline.commands import PkgCommand
from cmdline import ArgParser

def deb2cati(file_path: str) -> str:
    """
    Converts deb package to cati package and returns generated cati package file path

    Args:
        file_path: deb package filepath

    Returns:
        returns generated cati package filepath
    """
    file_path = os.path.abspath(file_path)
    tmp_dir = Temp.make_dir()
    cwd = os.getcwd()
    os.chdir(tmp_dir)
    try:
        shutil.copy(file_path, './package.deb')

        script = '''
        ar -x package.deb
        mkdir cati
        mkdir cati/control cati/scripts
        mv control.tar.* cati/control
        mkdir cati/files
        mv data.tar.* cati/files
        rm debian-binary package.deb
        touch cati/data.json
        '''.strip().split('\n')
        script = [l.strip() for l in script]

        for line in script:
            result = os.system(line)
            if result != 0:
                # script has error, return current filepath
                os.chdir(cwd)
                return file_path
        os.chdir('cati/control')
        os.system('tar -xf control.tar.*')
        os.system('rm control.tar.*')
        os.chdir('..')
        os.chdir('files')
        os.system('tar -xf data.tar.*')
        os.system('rm data.tar.*')
        os.chdir('..')

        # convert content data to cati json
        control_f = open('control/control', 'r').read()
        control_f_lines = control_f.strip().split('\n')
        control_fields = {}
        tmp_last_key = None
        for line in control_f_lines:
            if line != '':
                if line[0] == ' ':
                    if tmp_last_key != None:
                        control_fields[tmp_last_key] += '\n' + line
                else:
                    key = line.split(':', 1)[0]
                    value = line.split(':', 1)[1].strip()
                    tmp_last_key = key
                    control_fields[key] = value
        
        # convert control fields to cati data.json
        cati_data = {}
        for k in control_fields:
            # TODO : convert more fields
            if k == 'Package':
                cati_data['name'] = control_fields[k].strip()
            elif k == 'Version':
                cati_data['version'] = control_fields[k].strip()
            elif k == 'Architecture':
                cati_data['arch'] = control_fields[k].strip()
            elif k == 'Maintainer':
                cati_data['maintainer'] = control_fields[k].strip()
            elif k == 'Description':
                cati_data['description'] = control_fields[k]
            elif k == 'Homepage':
                cati_data['homepage'] = control_fields[k].strip()
            elif k == 'Section':
                cati_data['category'] = [control_fields[k].strip()]
            elif k == 'Suggests':
                cati_data['suggests'] = [tmp.strip() for tmp in control_fields[k].strip().split(',')]
        os.system('rm control -rf')
        cati_data_f = open('data.json', 'w')
        cati_data_f.write(json.dumps(cati_data))
        cati_data_f.close()
        os.chdir('..')
        
        # build pkg
        pkg_command = PkgCommand.PkgCommand()
        pkg_command.handle(ArgParser.parse(['cati', 'pkg', 'build', 'cati', '-q']))

        if os.path.isfile('cati.cati'):
            try:
                shutil.copy('cati.cati', file_path + '.cati')
                os.chdir(cwd)
                return file_path + '.cati'
            except:
                tmp_file_path = Temp.make_file()
                shutil.copy('cati.cati', tmp_file_path)
                return tmp_file_path
    except Exception as ex:
        print('error: ' + str(ex))
        os.chdir(cwd)
        return file_path

    os.chdir(cwd)
    return file_path

def rpm2cati(file_path: str) -> str:
    """
    Converts rpm package to cati package and returns generated cati package file path

    Args:
        file_path: rpm package filepath

    Returns:
        returns generated cati package filepath
    """
    # require alien
    if os.system('alien 2> /dev/null') != 256:
        return file_path

    file_path = os.path.abspath(file_path)
    cwd = os.getcwd()
    tmp_dir = Temp.make_dir()
    os.chdir(tmp_dir)

    try:
        shutil.copy(file_path, 'package.rpm')
        res = os.system('alien package.rpm 2> /dev/null')
        if res != 0:
            return file_path

        os.system('mv *.deb package.deb')

        rpm_path = file_path + '.deb'
        try:
            shutil.copy('package.deb', rpm_path)
        except:
            rpm_path = Temp.make_file()
            shutil.copy('package.deb', rpm_path)

        os.chdir(cwd)
        return deb2cati(rpm_path)
    except:
        os.chdir(cwd)
        return file_path
