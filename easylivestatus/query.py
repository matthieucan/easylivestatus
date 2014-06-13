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


import json

from easylivestatus.components import Column, ColumnContainer, \
     Filter, FilterContainer, \
     Stat, StatContainer, \
     Sort, SortContainer, \
     Groupby, GroupbyContainer

class Query(object):
    """
    Query is a wrapper around LiveStatus queries, and permits to
    construct complex requests while only using Python's syntax.

    >>> from easylivestatus.query import Query
    >>> q = (Query('hosts')
    ...      .columns('name', 'description')
    ...      .filters('state = 1')
    ...      .limit(42)
    ...     )
    >>> print(q)
    GET hosts
    Columns: name description
    Filter: state = 1
    ColumnHeaders: On
    >>>
    """
    def __init__(self, datasource=None):
        self._datasource = datasource
        self._columns = ColumnContainer()
        self._filters = FilterContainer()
        self._stats = StatContainer()
        self._sorts = SortContainer()
        self._groupby = GroupbyContainer()
        self._column_headers = None
        self._limit = None
        self._output_format = None

    def _check_type(self, name, obj, types):
        if not isinstance(types, list):
            types = [types]
        for t in types:
            if isinstance(obj, t):
                return True
        types_str = '/'.join([str(e) for e in types])
        msg = '%s (%s) must be %s, got %s instead.'
        msg %= (name, obj, types_str, str(type(obj)))
        raise ValueError(msg)
    
    def columns(self, *args):
        for arg in args:
            self._check_type('Columns', arg, str)
        self._columns.extend([Column(x) for x in args])
        return self
    
    def filters(self, *args):
        for arg in args:
            self._check_type('Filters', arg, str)
        self._filters.extend([Filter(x) for x in args])
        return self

    def stats(self, *args):
        for arg in args:
            self._check_type('Stats', arg, str)
        self._stats.extend([Stat(x) for x in args])
        return self

    def sorts(self, *args):
        for arg in args:
            self._check_type('Sorts', arg, str)
        self._sorts.extend([Sort(x) for x in args])
        return self
    
    def groupby(self, *args):
        for arg in args:
            self._check_type('Group by', arg, str)
        self._groupby.extend([Groupby(x) for x in args])
        return self

    def column_headers(self, val):
        self._check_type('Column headers', val, bool)
        self._column_headers = val
        return self

    def limit(self, val):
        self._check_type('Limit', val, int)
        self._limit = val
        return self
    
    def output_format(self, val):
        self._check_type('Output format', val, str)
        self._output_format = val
        return self

    def to_dict(self):
        d = {'datasource': self._datasource,
             'columns': [x.to_dict() for x in self._columns],
             'filters': [x.to_dict() for x in self._filters],
             'stats': [x.to_dict() for x in self._stats],
             'sorts': [x.to_dict() for x in self._sorts],
             'groupby': [x.to_dict() for x in self._groupby],
             'column_headers': self._column_headers,
             'limit': self._limit,
             'output_format': self._output_format,
             }
        return d
    
    def to_json(self):
        d = self.to_dict()
        return json.dumps(d)

    def from_dict(self, d):
        """ Warning: will override self attributes. """
        self._datasource = d.get('datasource', None)
        self._columns = ColumnContainer(d.get('columns', []))
        self._filters = FilterContainer(d.get('filters', []))
        self._stats = StatContainer(d.get('stats', []))
        self._sorts = SortContainer(d.get('sorts', []))
        self._groupby = GroupbyContainer(d.get('groupby', []))
        self._column_headers = d.get('column_headers', None)
        self._limit = d.get('limit', None)
        self._output_format = d.get('output_format', None)
        
        return self

    def from_json(self, content):
        d = json.loads(content)
        return self.from_dict(d)
    
    def __repr__(self):
        # datasource
        q = 'GET {0}\n'.format(self._datasource)
        
        # columns
        if self._columns:
            q += str(self._columns)
            
        # filters
        if self._filters:
            q += str(self._filters)

        # stats
        if self._stats:
            q += str(self._stats)
        
        # sorting
        if self._sorts:
            q += str(self._sorts)

        # groupby
        if self._groupby:
            q += str(self._groupby)

        # column headers
        if self._column_headers:
            q += 'ColumnHeaders: {0}\n'.format(
                {True: 'On', False: 'On'}[self._column_headers])

        # output format
        if self._output_format:
            q += 'OutputFormat: {0}\n'.format(self._output_format)
        
        return q

if __name__ == '__main__':
    q = (Query('foo')
         .columns('foo', 'bar')
         .filters('hey', 'ya')
         .stats('ploum', 'abcd')
         .sorts('lklk', 'klkl')
         .groupby('qwe', 'rty')
         .column_headers(True)
         .limit(42)
         .output_format('json')
         )
    print q
    from pprint import pprint
    pprint(q.to_dict())
    assert q.to_dict() == {'datasource': 'foo',
                           'columns': ['foo', 'bar'],
                           'filters': ['hey', 'ya'],
                           'stats': ['ploum', 'abcd'],
                           'sorts': ['lklk', 'klkl'],
                           'groupby': ['qwe', 'rty'],
                           'column_headers': True,
                           'limit': 42,
                           'output_format': 'json',
                           }
