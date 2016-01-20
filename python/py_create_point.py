#!/usr/bin/python
# coding=utf-8

from StringIO import StringIO
import sys
import os
import re

Usage = \
'''\
USAGE:
    command <DIR or x.png> [OUT_FILE]\
'''

xmlhead = \
'''\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/D
<plist version="1.0">
<dict>\
'''
xmltail = \
'''\
</dict>
</plist>\
'''

buf=StringIO()
temp=sys.stderr
sys.stderr=buf

def analysis(filename):
    iin,out = os.popen2('VertexScanner -r 1 -c 1 '+filename+' |sed "1,/.*/d"')
    content = out.readlines()
    if len(content)<=0: return None
    content = [ l.strip('\n') for l in content ]
    pattern = re.compile(r'-?\d+')
    print '\t<key>'+os.path.basename(filename)+'</key>' 
    print '\t<array>'
    blank = '\t'*3
    for line in content:
        point = pattern.findall(line)
        print '\t\t<dict>'
        print blank+'<key>x</key>'
        print blank+'<string>'+point[0]+'</string>'
        print blank+'<key>y</key>'
        print blank+'<string>'+point[1]+'</string>'
        print '\t\t</dict>'
    print '\t</array>'

def create_plist(dir, out=None):
    '''
        dir:png文件或者目录
        out:输出文件，默认为标准输出
    '''
    #重定向
    if out:
        if os.path.exists(out):
            print 'file '+out+' already exists'
            return None
        buf=open(out,'w')
        print 'd'
    else:
        buf=sys.stdout
    temp=sys.stdout
    sys.stdout=buf

    if os.path.isdir(dir):
        files = os.listdir(dir)
        files = re.findall('\w+?\.png',str(files))
        dir   = os.path.abspath(dir)
        print xmlhead
        for file in files:
            analysis(dir+os.sep+file)
        print xmltail
    elif re.search('\.png',dir):
        print xmlhead
        analysis(dir)
        print xmltail
    else:
        print 'not *.png or dir'
        return False
    
    #恢复重定向
    sys.stdout=temp
    return True


if __name__=='__main__':
    if len(sys.argv)<2:
        print Usage
        exit(0)
    file= sys.argv[2] if len(sys.argv)>2 else None
    if create_plist(sys.argv[1], file):
        print 'create file '+file+' successful'

