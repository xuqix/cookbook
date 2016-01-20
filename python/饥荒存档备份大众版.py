# -*- coding:utf-8 -*-

import sys
import wx
import os
from wx.lib.wordwrap import wordwrap
import shutil

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    backup_path     = ''
    recover_path    = '.\\remote_'

    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        backup = wx.Button(self, -1, u"备份", (50,48))
        self.Bind(wx.EVT_BUTTON, self.OnBackup, backup)

        recover= wx.Button(self, -1, u"还原", (50,78))
        self.Bind(wx.EVT_BUTTON, self.OnRecover, recover)

        if os.path.exists('.\\backup_path.ini'):
            TestPanel.backup_path   = open('.\\backup_path.ini').readline().strip()
        wx.StaticText(self, -1, u'存档当前路径:\n%s' % TestPanel.backup_path,   
                (10, 0)) 

    def OnBackup(self, evt):
        info = wx.AboutDialogInfo()

        try:
            # First we create and fill the info object
            if os.path.exists(TestPanel.recover_path) and os.path.exists(TestPanel.backup_path):
                shutil.rmtree(TestPanel.recover_path)

            shutil.copytree(TestPanel.backup_path,TestPanel.recover_path,True)
            # Then we call wx.AboutBox giving it that info object
            info.Name = u"备份成功"
            wx.AboutBox(info)
        except Exception,err:
            info.Name = u"备份失败"
            wx.AboutBox(info)
        
    def OnRecover(self, evt):
        info = wx.AboutDialogInfo()

        try:
            # First we create and fill the info object
            if not os.path.exists(TestPanel.recover_path):
                return
            try:
                shutil.rmtree(TestPanel.backup_path)
            except:
                pass

            shutil.copytree(TestPanel.recover_path,TestPanel.backup_path,True)
            # Then we call wx.AboutBox giving it that info object
            info.Name = u"还原成功"
            wx.AboutBox(info)
        except Exception,err:
            info.Name = u"还原失败"
            wx.AboutBox(info)

#----------------------------------------------------------------------

class MyFrame(wx.Frame):
    
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,-1,title,pos=(200,200),
                size=(200,180) )

        menuBar     = wx.MenuBar()

        fileMenu    = wx.Menu()
        fileMenu.Append(100,u"打开","choice file")


        menuBar.Append(fileMenu,u"选择备份文件")
        self.SetMenuBar(menuBar)

        #self.CreateStatusBar()

        self.Bind(wx.EVT_MENU,self.OnOpen,id=100)

        self.panel   = TestPanel(self, 'hello')

        

    def OnOpen(self,evt):
        # In this case we include a "New directory" button. 
        dlg = wx.DirDialog(self, u"请选择备份目录的路径:",
                          style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )

        # If the user selects OK, then we process the dialog's data.
        # This is done by getting the path data from the dialog - BEFORE
        # we destroy it. 
        if dlg.ShowModal() == wx.ID_OK:
            open('.\\backup_path.ini','w').write(dlg.GetPath())
            backup_path     = dlg.GetPath() 
            wx.StaticText(self.panel, -1, u'存档当前路径:\n%s'%backup_path,   
                (10, 0)) 
            
        # Only destroy a dialog after you're done with it.
        dlg.Destroy()


class MyApp(wx.App):

    def OnInit(self):
        frame   = MyFrame(None,u'饥荒备份')
        self.SetTopWindow(frame)
        frame.Show()
      
        return True


app     = MyApp(False)
app.MainLoop()


















