from base import *

DIR         = "x_forwarded_for_cgi_3"
REMOTE_IP   = "9.10.11.12"
REMOTE_PORT = "33112"

CONF = """
vserver!1!rule!2540!match = directory
vserver!1!rule!2540!match!directory = /%s
vserver!1!rule!2540!handler = cgi
vserver!1!rule!2540!handler!x_real_ip_enabled = 1
vserver!1!rule!2540!handler!x_real_ip_access_all = 0
vserver!1!rule!2540!handler!x_real_ip_access = ::1,127.0.0.1
""" % (DIR)

CGI_CODE = """#!/bin/sh

echo "Content-Type: text/plain"
echo

echo "REMOTE_ADDR ->${REMOTE_ADDR}<-"
echo "REMOTE_PORT ->${REMOTE_PORT}<-"
echo
"""

class Test (TestBase):
    def __init__ (self):
        TestBase.__init__ (self, __file__)
        self.name = "X-Forwared-For to REMOTE_ADDR: multiport"

        self.request           = "GET /%s/test HTTP/1.0\r\n" % (DIR)  + \
                                 "X-Forwarded-For: %s:%s, 9.9.9.9\r\n" % (REMOTE_IP, REMOTE_PORT)
        self.expected_error    = 200
        self.conf              = CONF
        self.proxy_suitable    = False

    def CustomTest (self):
        body = self.reply.split ("\r\n\r\n")[1]

        if "REMOTE_ADDR ->%s<-" %(REMOTE_IP) in body and \
           "REMOTE_PORT ->%s<-" %(REMOTE_PORT) in body:
            return 0

        return -1

    def Prepare (self, www):
        d = self.Mkdir (www, DIR, 0777)
        self.WriteFile (d, "test", 0555, CGI_CODE)
