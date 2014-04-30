# This file is part of easylivestatus.
# easylivestatus is a library to easily create LiveStatus queries.
#
# Copyright (C) 2014, Matthieu Caneill <matthieu.caneill@savoirfairelinux.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class Component(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

    def to_dict(self):
        return str(self)

class Container(list):
    def __repr__(self):
        raise NotImplementedError()

class Column(Component):
    pass

class ColumnContainer(Container):
    def __repr__(self):
        columns = ' '.join([str(x) for x in self])
        return 'Columns: {0}\n'.format(columns)

class Filter(Component):
    pass

class FilterContainer(Container):
    def __repr__(self):
        res = ''
        for x in self:
            res += 'Filter: {0}\n'.format(str(x))
        return res

class Stat(Component):
    pass

class StatContainer(Container):
    def __repr__(self):
        res = ''
        for x in self:
            res += 'Stats: {0}\n'.format(str(x))
        return res

class Sort(Component):
    pass

class SortContainer(Container):
    def __repr__(self):
        res = ''
        for x in self:
            res += 'Sort: {0}\n'.format(str(x))
        return res

class Groupby(Component):
    pass

class GroupbyContainer(Container):
    def __repr__(self):
        columns = ' '.join([str(x) for x in self])
        return 'Columns: {0}\n'.format(columns)
