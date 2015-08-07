#!/tools/bin/python
##!/usr/bin/python3
#

#<form method="post" name="networkmapdRefresh" action="/apply.cgi" target="hidden_frame">
#<input type="hidden" name="action_mode" value="update_client_list">
#<input type="hidden" name="action_script" value="">
#<input type="hidden" name="action_wait" value="1">
#<input type="hidden" name="current_page" value="httpd_check.xml">
#<input type="hidden" name="next_page" value="httpd_check.xml">
#<input type="hidden" name="client_info_tmp" value="">
#</form>

from asus import AsusDeviceScanner

#http://190.53.26.252/apply.cgi?refresh_networkmap

sc = AsusDeviceScanner('190.53.26.252','','*')
print(sc.client_connected('foo'))
print(sc.client_connected('MACBOOKAIR-EAFB'))
#print(sc.client_connected('android-8c4066f'))
