# -*- coding: utf-8 -*-

from common.mymako import render_mako_context, render_json
import re
import paramiko
import os
def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/home.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def getinfo(request):
    FilePath = '/gamedata/gamedata/'
    FileName = os.listdir(FilePath)
    fullfile = []
    for txtfile in FileName:
        fullfile.append(os.path.join(FilePath,txtfile))

    serIp = []
    time = []
    numon = []
    numoff = []
    date = 0
    for fullpath in fullfile:
        serIp.append([])
        time.append([])
        numon.append([])
        numoff.append([])
        f = open(fullpath, "r")
        lines = f.readlines()
        n = 0
        max = 0
        for line in lines:
            fg1 = 0
            sum = line.find(r'SUM')
            if sum >= 0:
                fg1 = 1
            line = line.rstrip('\n')
            head = line.find(r'>>>')
            tail = line.find(r'=')
            if (head != -1) & (tail != -1):
                time[date].append(line[head + 3:tail])

            head1 = line.find(r'id-')
            tail1 = line.find(r' ', head1)
            head2 = line.find(r'ip-')
            tail2 = line.find(r' ', head2)
            head3 = line.find(r'login-')
            tail3 = line.find(r' ', head3)
            head4 = line.find(r'offline-')
            # tail4 = line.find(r'\n')

            if (head1 != -1) & (tail1 != -1):
                num = line[head1 + 3:tail1]
                serID = int(num)
                if serID > max:
                    max = serID
                    numon[date].append([])
                    numoff[date].append([])
                    #print serID

            if (head2 != -1) & (tail2 != -1):
                IpAddr = line[head2 + 3:tail2]
                # print IpAddr
                if len(serIp[date]) < serID:
                    serIp[date].append(IpAddr)

            if fg1 == 0:
                if (head3 != -1) & (tail3 != -1):
                    numon[date][serID - 1].append(int(line[head3 + 6:tail3]))
                    # print line[head3+6:tail3]

                if head4 != -1:
                    numoff[date][serID - 1].append(int(line[head4 + 8:]))
                    # print line[head4+8:]
                    n = n + 1
        date = date + 1
    print serIp
    return render_json({'time':time,'ip':serIp, 'id':serID, 'login':numon, 'offline':numoff})
