# -*- coding: utf-8 -*-
# FileName: DNSCfg.py
# Author  : xiaoyao9933
# Email   : me@chao.lu
# Date    : 2013-02-14
# Vesion  : 1.2
import wmi
import _winreg
import os
from ctypes import *

class DNSCfg:
	def __init__(self):
		self.wmiService = wmi.WMI()
		self.netCfgBackup={}
		self.GetDNSBackup()
		print self.netCfgBackup
	#----------------------------------------------------------------------
	# Get the Adapter who has mac from wmi 
	#----------------------------------------------------------------------
	def GetDNSBackup(self):
		flag = False
		hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'System\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\',0,_winreg.KEY_ALL_ACCESS)
		keyInfo = _winreg.QueryInfoKey(hkey)
		for index in range(keyInfo[0]):
				hSubKeyName = _winreg.EnumKey(hkey, index)
				hSubKey = _winreg.OpenKey(hkey, hSubKeyName,0,_winreg.KEY_ALL_ACCESS)
				try:
					_winreg.QueryValueEx(hSubKey, 'T1')
					self.netCfgBackup[hSubKeyName]=_winreg.QueryValueEx(hSubKey, 'NameServer')[0]
					if '127.0.0.1' in self.netCfgBackup[hSubKeyName]:
						try:
							self.netCfgBackup[hSubKeyName]=_winreg.QueryValueEx(hSubKey, 'LastNameServer')[0]
						except:
							self.netCfgBackup[hSubKeyName]=u'8.8.8.8,8.8.4.4'
						flag = True
						print '>> Not normal closed last time , set dns to backup or 8.8.8.8.'
					else:
						_winreg.SetValueEx(hSubKey,'LastNameServer',None,_winreg.REG_SZ,self.netCfgBackup[hSubKeyName])					
				except:
					pass
		if flag:
			self.RestoreDns()
	#----------------------------------------------------------------------
	# Modify DNS
	#----------------------------------------------------------------------
	def ModifyDns(self,dns):
		for id in self.netCfgBackup:
			self.RegModifyDns(id,dns)
		self.colNicConfigs = self.wmiService.Win32_NetworkAdapterConfiguration(IPEnabled = True)
		for i in range(len(self.colNicConfigs)):
			if self.colNicConfigs[i].SetDNSServerSearchOrder(DNSServerSearchOrder = dns.split(','))[0] == 0:
				print '>> Modify Success!'
		print self.netCfgBackup
		return 0
	#----------------------------------------------------------------------
	# Restore DNS
	#----------------------------------------------------------------------
	def RestoreDns(self):
		flag = True
		for id in self.netCfgBackup:
			self.RegModifyDns(id,self.netCfgBackup[id])
			self.colNicConfigs = self.wmiService.Win32_NetworkAdapterConfiguration(SettingID = id, IPEnabled = True)
			for i in range(len(self.colNicConfigs)):
				if '.' in self.netCfgBackup[id]:
					tmp = self.netCfgBackup[id].split(',')
				else:
					tmp = []
				if self.colNicConfigs[i].SetDNSServerSearchOrder(DNSServerSearchOrder = tmp)[0] == 0:
					print '>> Restore Success!'
					flag = False
		if flag:
			DhcpNotifyConfigChange = windll.dhcpcsvc.DhcpNotifyConfigChange
			result = True
			for id in self.netCfgBackup:
				try:
					tmp = DhcpNotifyConfigChange(None, \
								id, \
								False, \
								0, \
								0, \
								0, \
								0)
					if tmp == 0:
						result =False
				except:
					pass
			if result:
				self.colNicConfigs = self.wmiService.Win32_NetworkAdapterConfiguration(IPEnabled = True)
				for i in range(len(self.colNicConfigs)):
					self.colNicConfigs[i].SetDNSServerSearchOrder(DNSServerSearchOrder = ['8.8.8.8','8.8.4.4'])
		print self.netCfgBackup
		return 0
	#----------------------------------------------------------------------
	# ModifyDns in Registry
	#----------------------------------------------------------------------
	def RegModifyDns(self,id,dns):
		print id,dns
		hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'System\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\',0,_winreg.KEY_ALL_ACCESS)
	
		hSubKey = _winreg.OpenKey(hkey, id,0,_winreg.KEY_ALL_ACCESS)
		print _winreg.SetValueEx(hSubKey,'NameServer',None,_winreg.REG_SZ,dns)
	
		#pass
		
def PrintInfo():
	print 'Registry Info:'
	hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'System\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\')
	keyInfo = _winreg.QueryInfoKey(hkey)
	for index in range(keyInfo[0]):
			hSubKeyName = _winreg.EnumKey(hkey, index)
				
			print hSubKeyName
			hSubKey = _winreg.OpenKey(hkey, hSubKeyName)
			try:
				print _winreg.QueryValueEx(hSubKey, 'NameServer')
			except:
				pass
	print 'WMI Info'
	wmiService = wmi.WMI()
	colNicConfigs = wmiService.Win32_NetworkAdapterConfiguration()
	for i in range(len(colNicConfigs)):
		print 'IPEnabled'
		print colNicConfigs[i].IPEnabled
		print 'SettingID' 
		print colNicConfigs[i].SettingID 
		print 'DNS' 
		print colNicConfigs[i].DNSServerSearchOrder