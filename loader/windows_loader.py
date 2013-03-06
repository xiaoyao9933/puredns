#! /usr/bin/python
# -*- coding: utf-8 -*-
# FileName: PureDNS.py
# Author  : xiaoyao9933
# Email   : me@chao.lu
# Date    : 2013-03-06
# Vesion  : 1.3
import wx
import webbrowser
import time
import _winreg
from server.tcpdns import TCPDNS
import os,sys,traceback 
import signal 
########################################################################
class Icon(wx.TaskBarIcon):
    TBMENU_SERVICE = wx.NewId()
    TBMENU_CLOSE   = wx.NewId()
    TBMENU_ABOUT  = wx.NewId()
    state=False
    version = '1.3'
    #----------------------------------------------------------------------
    def __init__(self,serv,dnscfg):
        wx.TaskBarIcon.__init__(self)
        self.menu = wx.Menu()
        self.menu.Append(self.TBMENU_SERVICE, "NULL")
        self.menu.Append(self.TBMENU_ABOUT, u"关于 PureDNS" + self.version)
        self.menu.AppendSeparator()
        self.menu.Append(self.TBMENU_CLOSE, u"退出程序")
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
        print 'there1'
        self.serv.run()
        self.dnscfg = dnscfg
        time.sleep(1)
        print 'there'
        if self.serv.server:
            self.state = True
            self.dnscfg.modify('127.0.0.1')
            self.menu.SetLabel(self.TBMENU_SERVICE,u'停用DNS代理')
        else:
            self.state = False
            wx.MessageDialog(None,u'端口号53已经被占用',u'错误',wx.OK).ShowModal()
            self.menu.SetLabel(self.TBMENU_SERVICE,u'启动DNS代理') 

    #----------------------------------------------------------------------
    def OnTaskBarSevice(self,evt):
        if self.state is False:
            self.dnscfg.modify('127.0.0.1')
            self.state=True
            self.menu.SetLabel(self.TBMENU_SERVICE,u'停用DNS代理')
        else:
            self.dnscfg.restore()
            self.state=False
            self.menu.SetLabel(self.TBMENU_SERVICE,u'启动DNS代理')         
 
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
    def __init__(self, logfile,notadmin,cfg,redirect=False, filename=None):
        self.logfile=logfile
        self.notadmin = notadmin
        self.hdnscfg = cfg
        wx.App.__init__(self, redirect, filename)

    def OnInit(self):
        if False:
            wx.MessageDialog(None,u'请以管理员权限运行本程序',u'错误',wx.OK).ShowModal()
            self.ExitMainLoop()
            return True
        self.htcpdns = TCPDNS(self.hdnscfg)
        if self.notadmin:
            wx.MessageDialog(None,u'请以管理员权限运行本程序',u'错误',wx.OK).ShowModal()
            self.htcpdns.force_close()
            self.ExitMainLoop()
            return True
        self.frame = Frame(None)
        #.Bind(wx.EVT_CLOSE,self.OnExit)
        #self.Bind(wx.EVT_END_SESSION,self.OnExit)
        return True
    def OnExit(self):
        self.hdnscfg.restore()
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
def load(cfg):
    firstrun=False
    notadmin=False
    global logfile

    try:
        hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\\xiaoyao9933')
        firstrun = False
    except:
        try:
            hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\\',0,_winreg.KEY_ALL_ACCESS)
            _winreg.CreateKey(hkey, 'xiaoyao9933')
        except:
            notadmin=True
        firstrun = True
    if firstrun:
        webbrowser.open('https://github.com/xiaoyao9933/puredns/wiki/%E6%AC%A2%E8%BF%8E%E4%BD%BF%E7%94%A8PureDNS')
    try:
        logfile=open('log.txt','w')
        sys.stdout = logfile
        sys.stderr = logfile
        try:
            app = App(logfile, notadmin, cfg)
            app.MainLoop()
        except:
            traceback.print_exc()
            #DNSCfg.PrintInfo()
            logfile.flush()
            wx.MessageDialog(None,u'遇到致命错误，请将同目录下的log.txt发送到puredns@chao.lu,多谢!',u'错误',wx.OK).ShowModal()
            
    finally:
        sys.stdout = logfile
        sys.stderr = logfile
        print '>> Finally closed'
        try:
            logfile.close()
        except:
            pass
        os._exit(0)
	

