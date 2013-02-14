#! /usr/bin/python
# -*- coding: utf-8 -*-
# FileName: PureDNS.py
# Author  : xiaoyao9933
# Email   : me@chao.lu
# Date    : 2013-02-14
# Vesion  : 1.2
import wx
import webbrowser
import time
import DNSCfg
import tcpdns
import _winreg
import os,sys,traceback 
import signal 
########################################################################
class Icon(wx.TaskBarIcon):
    TBMENU_SERVICE = wx.NewId()
    TBMENU_CLOSE   = wx.NewId()
    TBMENU_ABOUT  = wx.NewId()
    state=False
    version = '1.2'
    #----------------------------------------------------------------------
    def __init__(self,serv,dnscfg):
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
        self.Bind(wx.EVT_MENU, self.OnClose, id=self.TBMENU_CLOSE)
        self.Bind(wx.EVT_MENU, self.OnTaskBarSevice, id=self.TBMENU_SERVICE)
        self.Bind(wx.EVT_MENU, self.OnTaskBarAbout, id=self.TBMENU_ABOUT)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarClick)
        self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.OnTaskBarClick)
        self.serv = serv 
        self.serv.start()
        self.dnscfg = dnscfg
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
    def OnTaskBarActivateD(self, evt):
        """"""
        pass
 
    #----------------------------------------------------------------------

    def OnClose(self, evt): 
        self.RemoveIcon()
        self.menu.Destroy()
        self.Destroy()
        wx.Exit()
        print '>> Destoryted'
    	
    #----------------------------------------------------------------------
    def OnTaskBarClick(self, evt):
        """
        Create the click menu
        """
        self.PopupMenu(self.menu)
    #def CreatePopupMenu(self):
  #      return self.menu
    def OnTaskBarAbout(self, evt):
        """
        Create the about dialog
        """
        webbrowser.open('https://github.com/xiaoyao9933/puredns/wiki/%E6%AC%A2%E8%BF%8E%E4%BD%BF%E7%94%A8PureDNS')
class Frame(wx.Frame):
    def __init__(self, *args, **kwargs): 
        super(Frame, self).__init__(*args, **kwargs) 
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.tbIcon = Icon(wx.GetApp().htcpdns, wx.GetApp().hdnscfg)
    def onClose(self,evt):
        print '>> OnClose()'
        logfile.flush()
        wx.GetApp().OnExit()

        
class App(wx.App):
    def __init__(self, logfile,redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.logfile=logfile
    def OnInit(self):
        self.htcpdns = tcpdns.tcpdns()
        self.hdnscfg = DNSCfg.DNSCfg()
        self.frame = Frame(None)
        #.Bind(wx.EVT_CLOSE,self.OnExit)
        #self.Bind(wx.EVT_END_SESSION,self.OnExit)
        return True
    def OnExit(self):
        self.hdnscfg.RestoreDns()
        self.htcpdns.force_close()
        print '>> OnExit()'
        logfile.flush()
        self.ExitMainLoop()
        
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
    firstrun=False
    global logfile

    try:
        hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\\xiaoyao9933')
        firstrun = False
    except:
        hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\\')
        _winreg.CreateKey(hkey, 'xiaoyao9933')
        firstrun = True
    if firstrun:
        webbrowser.open('https://github.com/xiaoyao9933/puredns/wiki/%E6%AC%A2%E8%BF%8E%E4%BD%BF%E7%94%A8PureDNS')
    try:
        logfile=open('log.txt','w')
        sys.stdout = logfile
        sys.stderr = logfile
        try:
            app=App(logfile)
            app.MainLoop()
        except:
            traceback.print_exc()
            DNSCfg.PrintInfo()
            logfile.flush()
            wx.MessageDialog(None,'发生致命错误，请将与软件同目录下的 log.txt 发到 puredns@chao.lu,协助我完善程序，多谢!','错误',wx.OK).ShowModal()
            
    finally:
        sys.stdout = logfile
        sys.stderr = logfile
        print '>> Finally closed'
        try:
            logfile.close()
        except:
            pass
        os._exit(0)
	

