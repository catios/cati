#
# PkgConvertor.py
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

""" Deb and Rpm to cati package convertor """

import os
import sys
import shutil
import json
from cati.frontend import Temp
from cati.cmdline.commands import PkgCommand
from cati.cmdline import ArgParser

def convert_depends_list(debian_depends_control_value: str) -> list:
    """
    Converts the debian control file `depends/conflicts` items syntax to cati depends/conflicts list

    Args:
        debian_depends_control_value (str): value of package debian control field

    Returns:
        list: the list of depends/conflicts (converted to cati strcture)
    """
    depends_list = debian_depends_control_value.strip().split(',')
    depends_list = [item.strip().split('|') for item in depends_list]
    cati_data_json_list = []

    for item in depends_list:
        current_item = ''
        for part in item:
            part = part.strip()
            part_parts = part.split(' ', 1)
            pkg_name = part_parts[0]
            pkg_name = pkg_name.split(':')[0]
            version_part = None
            if len(part_parts) > 1:
                version_part = part_parts[1]
                version_part = version_part.strip().strip('(').strip(')')
                version_part = version_part.replace('>>', '>')
                version_part = version_part.replace('<<', '<')
            current_item += pkg_name + ' '
            if version_part:
                current_item += str(version_part)
            current_item += '| '
        current_item = current_item.strip()
        current_item = current_item[:len(current_item)-1]
        current_item = current_item.strip()
        cati_data_json_list.append(current_item)

    return cati_data_json_list

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

        # convert scripts
        if os.path.isfile('control/preinst'):
            shutil.copy('control/preinst', 'scripts/ins-before')

        if os.path.isfile('control/postinst'):
            shutil.copy('control/postinst', 'scripts/ins-after')

        if os.path.isfile('control/prerm'):
            shutil.copy('control/prerm', 'scripts/rm-before')

        if os.path.isfile('control/postrm'):
            shutil.copy('control/postrm', 'scripts/rm-after')

        # convert control fields to cati data.json
        cati_data = {}
        for k in control_fields:
            if k == 'Package':
                cati_data['name'] = control_fields[k].strip()
            elif k == 'Version':
                cati_data['version'] = control_fields[k].strip()
            elif k == 'Architecture':
                cati_data['arch'] = control_fields[k].strip()
            elif k == 'Maintainer':
                cati_data['maintainer'] = control_fields[k].strip()
            elif k == 'Original-Maintainer':
                cati_data['X-Original-Maintainer'] = control_fields[k].strip()
            elif k == 'Uploaders':
                cati_data['uploaders'] = control_fields[k].strip().split(',')
                cati_data['uploaders'] = [a.strip() for a in cati_data['uploaders']]
            elif k == 'Description':
                cati_data['description'] = control_fields[k]
            elif k == 'Changed-By':
                cati_data['changed-by'] = control_fields[k]
            elif k == 'Changes':
                cati_data['changes'] = control_fields[k]
            elif k == 'Date':
                cati_data['date'] = control_fields[k]
            elif k == 'Urgency':
                cati_data['urgency'] = control_fields[k]
            elif k == 'Essential':
                cati_data['essential'] = control_fields[k]
                if cati_data['essential'] == 'yes' or cati_data['essential'] == 'Yes':
                    cati_data['essential'] = True
                else:
                    cati_data['essential'] = False
            elif k == 'Homepage':
                cati_data['homepage'] = control_fields[k].strip()
            elif k == 'Section':
                cati_data['category'] = [control_fields[k].strip()]
            elif k == 'Depends' or k == 'Pre-Depends':
                try:
                    cati_data['depends']
                except:
                    cati_data['depends'] = []
                cati_data['depends'] = [*cati_data['depends'], *convert_depends_list(control_fields[k].strip())]
            elif k == 'Conflicts' or k == 'Breaks':
                try:
                    cati_data['conflicts']
                except:
                    cati_data['conflicts'] = []
                cati_data['conflicts'] = [*cati_data['conflicts'], *convert_depends_list(control_fields[k].strip())]
            elif k == 'Recommends':
                cati_data['recommends'] = convert_depends_list(control_fields[k].strip())
            elif k == 'Replaces':
                cati_data['replaces'] = convert_depends_list(control_fields[k].strip())
            elif k == 'Suggests':
                cati_data['suggests'] = convert_depends_list(control_fields[k].strip())
                cati_data['suggests'] = [item_tmp.split(' ')[0] for item_tmp in cati_data['suggests']]
            elif k == 'Enhances':
                cati_data['enhances'] = convert_depends_list(control_fields[k].strip())
                cati_data['enhances'] = [item_tmp.split(' ')[0] for item_tmp in cati_data['enhances']]
            elif k == 'Provides':
                cati_data['provides'] = convert_depends_list(control_fields[k].strip())
                cati_data['provides'] = [item_tmp.split(' ')[0] for item_tmp in cati_data['provides']]
            elif k[0] == 'X' or k[0] == 'x':
                cati_data[k] = control_fields[k].strip()
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
