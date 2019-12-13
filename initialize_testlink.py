from testlink import TestlinkAPIClient, TestLinkHelper
import sys

URL = 'http://localhost/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
DEVKEY = '68eaccc81c42b4aaaba9fb973f6cec70'

tl_helper = TestLinkHelper()
myTestLink = tl_helper.connect(TestlinkAPIClient)
myTestLink.__init__(URL, DEVKEY)

print(myTestLink.countProjects())