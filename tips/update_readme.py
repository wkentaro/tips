#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re


def get_rst_h1(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    h_pattern = re.compile('[-=\^]')
    for i, line in enumerate(lines):
        if h_pattern.match(line):
            if i == 0:
                title = lines[i+1].strip()
            if line[i-1].strip() != '':
                title = lines[i-1].strip()
            else:
                title = lines[i+1].strip()
            break
    return title


def get_date(filename):
    pattern = re.compile('^\d{4,4}-\d{1,2}-\d{1,2}')
    m = pattern.match(filename)
    date = filename[m.start():m.end()]
    return date


def get_index():
    files = os.listdir('.')
    pattern = re.compile('^\d{4,4}-\d{1,2}-\d{1,2}-.*')
    for tip_dir in files:
        if not (os.path.isdir(tip_dir) and pattern.match(tip_dir)):
            continue
        date = get_date(tip_dir)
        filename = os.path.join(tip_dir, 'README.rst')
        title = get_rst_h1(filename)
        line = '* `{label} <{url}>`_ ({date})'
        url = os.path.join('tips', filename)
        line = line.format(label=title, url=url, date=date)
        yield line


def main():
    lines = ['====', 'Tips', '====']
    lines.append('')  # space
    index_list = get_index()
    lines.extend(reversed(list(index_list)))  # index
    lines.append('')  # new lines at EOF

    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_dir, '../README.rst'), 'w') as f:
        f.write('\n'.join(lines))


if __name__ == '__main__':
    main()