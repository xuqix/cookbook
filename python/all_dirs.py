#!/usr/bin/env python

def allDirs(path):
    dirs = []
    for l in os.listdir(path):
        ll = os.path.join(path, l)
        if os.path.isdir(ll):
            dirs.append(ll)
            dirs += allDirs(ll)
    return dirs
