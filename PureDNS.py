#! /usr/bin/python
# -*- coding: utf-8 -*-
# FileName: PureDNS.py
# Author  : xiaoyao9933
# Email   : me@chao.lu
# Date    : 2013-02-13
# Vesion  : 1.1
import wx
import webbrowser
import time
import DNSCfg
import tcpdns
import _winreg
import os,sys,traceback  
########################################################################
class Icon(wx.TaskBarIcon):
    TBMENU_SERVICE = wx.NewId()
    TBMENU_CLOSE   = wx.NewId()
    TBMENU_ABOUT  = wx.NewId()
    state=False
    version = '1.1'
    #----------------------------------------------------------------------
    def __init__(self):
        wx.TaskBarIcon.__init__(self)
        self.menu = wx.Menu()
        self.menu.Append(self.TBMENU_SERVICE, "控制代理")
        self.menu.Append(self.TBMENU_ABOUT, "帮助 PureDNS" + self.version)
        self.menu.AppendSeparator()
        self.menu.Append(self.TBMENU_CLOSE,   "退出")
		# Set the image
        self.tbIcon = wx.EmptyIcon()
        self.tbIcon.LoadFile(resource_path("PureDNS.ico"),wx.BITMAP_TYPE_ICO) 
        self.SetIcon(self.tbIcon, "PureDNS")
        # bind some events
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.TBMENU_CLOSE)
        self.Bind(wx.EVT_MENU, self.OnTaskBarSevice, id=self.TBMENU_SERVICE)
        self.Bind(wx.EVT_MENU, self.OnTaskBarAbout, id=self.TBMENU_ABOUT)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarClick)
        self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.OnTaskBarClick)
        self.serv = tcpdns.tcpdns()
        self.serv.start()
        self.dnscfg = DNSCfg.DNSCfg()
        time.sleep(1)
        if self.serv.server:
            self.state = True
            self.dnscfg.ModifyDns('127.0.0.1')
            self.menu.SetLabel(self.TBMENU_SERVICE,'停止DNS代理')
        else:
            self.state = False
            wx.MessageDialog(None,'已经有其他进程占用53端口','错误',wx.OK).ShowModal()
            self.menu.SetLabel(self.TBMENU_SERVICE,'启动DNS代理') 

    #----------------------------------------------------------------------
    def OnTaskBarSevice(self,evt):
        if self.state is False:
            self.dnscfg.ModifyDns('127.0.0.1')
            self.state=True
            self.menu.SetLabel(self.TBMENU_SERVICE,'停止DNS代理')
        else:
            self.dnscfg.RestoreDns()
            self.state=False
            self.menu.SetLabel(self.TBMENU_SERVICE,'启动DNS代理')         
 
    #----------------------------------------------------------------------
    def OnTaskBarActivate(self, evt):
        """"""
        pass
 
    #----------------------------------------------------------------------
    def OnTaskBarClose(self, evt):
        """
        Destroy the taskbar icon and frame from the taskbar icon itself
        """
        self.dnscfg.RestoreDns()
        self.serv.force_close()
        self.RemoveIcon()
        self.menu.Destroy()
        self.Destroy()
        print '>> Destoryted' 
    #----------------------------------------------------------------------
    def OnTaskBarClick(self, evt):
        """
        Create the click menu
        """
        self.PopupMenu(self.menu)
    def OnTaskBarAbout(self, evt):
        """
        Create the about dialog
        """
        webbrowser.open('http://chao.lu/software/PureDns.php?version='+self.version)
		
 
########################################################################
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    firstrun=False
    global version
    version = '1.1'
	

    try:
        hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\\xiaoyao9933')
        firstrun = False
    except:
        hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\\')
        _winreg.CreateKey(hkey, 'xiaoyao9933')
        firstrun = True
    if firstrun:
        webbrowser.open('http://chao.lu/software/PureDns.php?version='+version)
    try:
        logfile=open('log.txt','w')
        sys.stdout = logfile
        sys.stderr = logfile
        try:
            tbIcon = Icon()
            app.MainLoop()
        except:
            traceback.print_exc()
            DNSCfg.PrintInfo()
            logfile.flush()
            wx.MessageDialog(None,'发生致命错误，请将与软件同目录下的 log.txt 发到 puredns@chao.lu,协助我完善程序，多谢!','错误',wx.OK).ShowModal()
            
    finally:
        logfile.close()
        os._exit(0)
        
	

