# -*- coding: utf-8 -*-
# FileName: DNSCfg.py
# Author  : xiaoyao9933
# Email   : me@chao.lu
# Date    : 2013-02-13
# Vesion  : 1.1
import wmi
import _winreg
import os

class DNSCfg:
	def __init__(self):
		self.wmiService = wmi.WMI()
		self.netCfgBackup={}
		self.GetAdapters()
		print self.netCfgBackup
		self.GetDNSBackup()
		self.CheckError()
	#----------------------------------------------------------------------
	# Get the Adapter who has mac from wmi 
	#----------------------------------------------------------------------
	def GetAdapters(self):
		hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'System\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\')
		keyInfo = _winreg.QueryInfoKey(hkey)
		for index in range(keyInfo[0]):
				hSubKeyName = _winreg.EnumKey(hkey, index)
				hSubKey = _winreg.OpenKey(hkey, hSubKeyName)
				try:
					_winreg.QueryValueEx(hSubKey, 'T1')
					self.netCfgBackup[hSubKeyName]=_winreg.QueryValueEx(hSubKey, 'NameServer')
				except:
					pass
	#----------------------------------------------------------------------
	# If the DNS contains '127.0.0.1', it means unexpected exit appeared last time.
	#----------------------------------------------------------------------
	def CheckError(self):
		flag = False
		for id in self.netCfgBackup:
			if '127.0.0.1' in self.netCfgBackup[id]:
				self.netCfgBackup[id]=''
				flag =True
				print '>> Error detected , set dns to dhcp method.'
		if flag:
			self.RestoreDns()
		
	#----------------------------------------------------------------------
	# Get DNS Backup
	#----------------------------------------------------------------------
	def GetDNSBackup(self):
		hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'System\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\')
		for id in self.netCfgBackup:
			try:
				hSubKey = _winreg.OpenKey(hkey, id)
				try:
					nameserver = _winreg.QueryValueEx(hSubKey, 'NameServer')[0]
				except:
					print 'NameServer key not found,pass'
					nameserver = ''
				self.netCfgBackup[id] = nameserver
			except:
				pass
		print self.netCfgBackup
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
			self.colNicConfigs = self.wmiService.Win32_NetworkAdapterConfiguration(IPEnabled = True)
			for i in range(len(self.colNicConfigs)):
				self.colNicConfigs[i].SetDNSServerSearchOrder(DNSServerSearchOrder = [])
			
		return 0
	#----------------------------------------------------------------------
	# ModifyDns in Registry
	#----------------------------------------------------------------------
	def RegModifyDns(self,id,dns):
		hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'System\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\')
		try:
			hSubKey = _winreg.OpenKey(hkey, id)
			_winreg.SetValue(hSubKey,'NameServer',_winreg.REG_SZ,dns)
		except:
			pass
		
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