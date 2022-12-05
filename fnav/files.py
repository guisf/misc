# -*- coding: utf-8 -*-

"""This file contain classes used to obtain information about files and
to build a file manager class.

"""

import os
import shutil
import re
import stat
import time
import pwd
import grp
import math


class PathInfo(object):
    """Collect all the information about a path.
    Mainly this is used to output a line like `ls -lh`, but in a purely
    python way.

    """

    def __init__(self, path):
        self.dir = os.path.dirname(path)
        self.name = os.path.basename(path)
        self.ext = os.path.splitext(self.name)[1].strip('.')
        data = os.lstat(path)
        self.mode = data[0]
        self.uid = data[4]
        self.gid = data[5]
        self.size = data[6] 
        self.atime = data[7]
        self.mtime = data[8]
        self.ctime = data[9]

    def __repr__(self):
        return "%s %s" % self.repr()

    def __cmp__(self, other):
        return cmp(other.mtime, self.mtime) or \
               cmp(self.name.lower(), other.name.lower())

    def repr(self):
        return ('%s%s %8s %8s %7s %s' % (self.type(), self.chmode(),
                                         self.owner(), self.group(), 
                                         self.hsize(), self.modifiedtime()), 
                self.name)

    def chmode(self):
        out = ''
        for who in ('USR', 'GRP', 'OTH'):
            for perm in ('R', 'W', 'X'):
                if self.mode & getattr(stat, 'S_I' + perm + who, 0):
                    out += perm.lower()
                else:
                    out += '-'
        return out

    def lstype(self):
        conv = {'d': 'di', 'l': 'ln', '-': 'fi', 'p': 'pi', 's': 'so',
                'b': 'bd', 'c': 'cd'}
        type = self.type()
        if self.binary():
            return 'ex'
        else:
            return conv[type]

    def type(self):
        map = { 'd': stat.S_ISDIR, 'b': stat.S_ISBLK, 'c': stat.S_ISCHR, 
                'p': stat.S_ISFIFO, 's': stat.S_ISSOCK, 'l': stat.S_ISLNK,
                '-': stat.S_ISREG }
        out = '?'
        for char, func in map.items():
            if func(self.mode):
                out = char
                break
        return out

    def owner(self):
        return pwd.getpwuid(self.uid)[0]

    def group(self):
        return grp.getgrgid(self.gid)[0]

    def modifiedtime(self):
        return self.clock(self.mtime)

    def createdtime(self):
        return self.clock(self.ctime)

    def acessedtime(self):
        return self.clock(self.atime)

    def hsize(self):
        if not self.size:
            return '0'
        unit = ",K,M,G,T,P,E,Z,Y".split(',')
        base = math.floor(math.log(self.size, 1024))
        value = float(self.size)/math.pow(1024, base)
        return '%.1f%s' % (value, unit[int(base)])

    def clock(self, seconds):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(seconds))
    
    def readable(self):
        return os.access(os.path.join(self.dir, self.name), os.R_OK)

    def writeable(self):
        return os.access(os.path.join(self.dir, self.name), os.W_OK)

    def executable(self):
        return os.access(os.path.join(self.dir, self.name), os.X_OK)

    def binary(self):
        return self.type() == '-' and self.executable()


class FileManager(object):
    """This class implements a basic file manager.
    It's methods will do some specific action uppon the files inside the
    current directory.
    
    """

    def __init__(self, dir):
        self.cwd = os.path.abspath(dir)
        self.contents = []  # will be a list of PathInfo objects
        self.names = []     # will contain only path names
        self.selected = []  # selected items
        self.option = ''    # any combination of [atr], like ls -atr
        self.regex = ''     # filter by regular expression

    def refilter(self, list):
        return [name for name in list if re.match(r'%s' % self.regex, name)]

    def setcontents(self):
        if 'a' not in self.option:
            cont = [a for a in os.listdir(self.cwd) if not a.startswith('.')]
        else:
            cont = os.listdir(self.cwd)
        
        if self.regex:
            cont = self.refilter(cont)
        
        if 't' not in self.option:
            cont.sort(lambda a, b: cmp(a.lower(), b.lower()))
            self.names = cont
        
        self.contents = []
        for c in cont:
            path = os.path.join(self.cwd, c)
            self.contents.append(PathInfo(path))
        
        if 't' in self.option:
            self.contents.sort()
            self.names = [f.name for f in self.contents]
        if 'r' in self.option:
            self.contents.reverse()
            self.names.reverse()

    def repr(self):
        return [a.repr() for a in self.contents]

    def select(self, j):
        if j not in self.selected:
            self.selected.append(j)
        else:
            self.selected.remove(j)

    def selectall(self):
        if len(self.selected) == len(self.contents):
            self.selected = []
        else:
            self.selected = []
            for j in range(len(self.contents)):
                self.selected.append(j)

    def delete(self):
        for j in self.selected[:]:
            f = self.contents[j]
            path = os.path.join(self.cwd, f.name)
            if f.type() == 'd':
                shutil.rmtree(path)
            else:
                os.remove(path)
            self.selected.remove(j)

    def copy(self, dest):
        dest = dest.rstrip(os.sep)
        if not dest.startswith(os.sep):
            dest = os.path.join(self.cwd, dest)
        if os.access(dest, os.F_OK):
            if os.path.isdir(dest):
                type = 'dir'
            else:
                type = 'file'
        else:
            type = ''
        for j in self.selected[:]:
            f = self.contents[j]
            src = os.path.join(self.cwd, f.name)
            to = dest
            if type == 'dir':
                to = os.path.join(dest, f.name)
            elif type == 'file':
                os.remove(dest)
            if f.type() == 'd':
                shutil.copytree(src, to, symlinks=True)
            else:
                shutil.copy(src, to)
            self.selected.remove(j)

    def mkdir(self, dirname):
        dirname = dirname.rstrip(os.sep)
        if not dirname.startswith(os.sep):
            dirname = os.path.join(self.cwd, dirname)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

    def mvselected(self, newname):
        newname = newname.rstrip(os.sep)
        if not newname.startswith(os.sep):
            newname = os.path.join(self.cwd, newname)
        for j in self.selected[:]:
            f = self.contents[j]
            oldname = os.path.join(self.cwd, f.name)
            shutil.move(oldname, newname)
            self.selected.remove(j)

