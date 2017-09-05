# -*- coding: utf-8 -*-

from common.mymako import render_mako_context, render_json

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
    #FilePath = 'C:\\Users\\Administrator\\Documents\\Tencent Files\\707257663\\FileRecv\\stats'
    FilePath = '/gamedata/gamedata/'
    FileName = os.listdir(FilePath)
    fullfile = []
    filedate = []
    for txtfile in FileName:
        fullfile.append(os.path.join(FilePath,txtfile))
        filedate.append(txtfile[6:16])
    serIp = []
    time = []
    numon = []
    numoff = []
    Anumon = []
    Anumoff = []
    Alogin = []
    Aoffline = []
    date = 0
    for fullpath in fullfile:
        serIp.append([])
        time.append([])
        numon.append([])
        numoff.append([])
        Anumoff.append([])
        Anumon.append([])
        f = open(fullpath, "r")
        lines = f.readlines()
        n = 0
        max = 0
        for line in lines:
            fg1 = 0
            sum1 = line.find(r'SUM')
            if sum1 >= 0:
                fg1 = 1
                head5 = line.find(r'login-')
                tail5 = line.find(r' ', head5)
                head6 = line.find(r'offline-')
                Anumon[date].append(int(line[head5 + 6: tail5]))
                Anumoff[date].append(int(line[head6 + 8:]))

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
        Alogin.append(float(sum(Anumon[date])/len(Anumon[date])))
        Aoffline.append(float(sum(Anumoff[date])/len(Anumoff[date])))
        date = date + 1
    print serIp
    return render_json({'time':time,'ip':serIp, 'id':serID, 'login':numon, 'offline':numoff, 'Alogin':Alogin, 'Aoffline':Aoffline, 'filename':filedate})