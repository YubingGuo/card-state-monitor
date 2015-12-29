import wx
import wx.grid
import logging
import data_types
import configurator
import card_controller

TARGET_IP_DCT0 = "192.168.129.2"
TARGET_IP_DCT1 = "192.168.130.10"

class CardStateGrid(wx.grid.Grid):
    def __init__(self, parent, id = -1, pos = wx.DefaultPosition, size = wx.DefaultSize):
        wx.grid.Grid.__init__(self, parent, id, pos, size)
        
        self.colCount = 6;
        self.content = data_types.CardList()
        self.ignoreUninst = False
        self.states = ("Installed", "Basic", "Fault", "Use", "Ne", "Specific")

        self.cards = ("lcp-0", "lcp-1", "lsp-0", "lsp-1", "lsp-2", "lsp-3", "lsp-4", 
                      "lsp-5", "lsp-6", "lsp-7", "lsp-8", "lsp-9", "lsp-10", "lsp-11",
                      "lsp-12", "lsp-13", "lsp-14", "lsp-15", "lca", "lbi", "lbr-0",
                      "lbr-1", "lbr-2", "lbr-3", "lni-0", "lni-1", "lps-0", "lps-1",
                      "lps-2", "lps-3", "lps-4", "lps-5")
                      
        self.menu_titles = [ "S-Reset",
                             "H-Reset",
                             "Block",
                             "Unblock",
                             "Sleep",
                             "Sleep Release"
                           ]

        self.colorMap = {data_types.STATE_TYPE_INVALID       : "GREY",
                         data_types.STATE_TYPE_UNINST        : "GREY",
                         data_types.STATE_TYPE_HIZ           : "DARK GREY",
                         data_types.STATE_TYPE_NOHWINFO      : "DARK SLATE GREY",
                         data_types.STATE_TYPE_INST          : "DARK GREEN",
                         data_types.STATE_TYPE_ACT           : "GREEN",
                         data_types.STATE_TYPE_BLOCK         : "BLUE",
                         data_types.STATE_TYPE_PBLOCK        : "MEDIUM BLUE",
                         data_types.STATE_TYPE_NOT_READY     : "SKY BLUE",
                         data_types.STATE_TYPE_CHECK         : "PINK",
                         data_types.STATE_TYPE_FULL_ALAMR    : "RED",
                         data_types.STATE_TYPE_PARTIAL_ALARM : "CORAL",
                         data_types.STATE_TYPE_SLEEP         : "PURPLE"}

        self.menu_title_by_id = {}
        for title in self.menu_titles:
            self.menu_title_by_id[wx.NewId()] = title

        self.selected_card = None
        self.cardController = card_controller.CardController(r'C:\eATT_2.7.0_LRC')

        self.InitView()
            
    def InitView(self):
        self.CreateGrid(0, self.colCount)
        self.SetLabelBackgroundColour("white")

        self.SetColLabelSize(32)
        self.SetRowLabelSize(40)
        self.SetColSize(0, 100)
        self.SetDefaultRowSize(20)
        self.SetRowLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)
        self.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)

        for col_index in range(self.colCount):
            self.SetColLabelValue(col_index, self.states[col_index])
    
    """for card in self.cards:
            self.AppendRows(1, True)
            row_index = self.GetNumberRows() - 1
            self.SetRowLabelValue(row_index, card)
            
            for col_index in range(self.colCount):
                self.SetCellValue(row_index, col_index, "-")"""

    def OnCellRightClick(self, event):
        self.selected_card = self.GetRowLabelValue(event.GetRow())

        menu = wx.Menu()
        for (id,title) in self.menu_title_by_id.items():
            menu.Append(id, title)
            self.Bind(wx.EVT_MENU, self.MenuSelectionCb, id=id)

        self.PopupMenu(menu, event.GetPosition())
        menu.Destroy()

    def ShowDialog(self, message, style):
        dlg = wx.MessageDialog(self, message, "Result", style)
        dlg.CenterOnParent()
        dlg.ShowModal()
        dlg.Destroy()

    def MenuSelectionCb( self, event ):
        operation = self.menu_title_by_id[event.GetId()]
        (ret, info) = self.cardController.Control(self.selected_card, operation)


        if(ret):
            message = operation + " " + self.selected_card + " successfully!"
            style = wx.OK | wx.ICON_INFORMATION | wx.CENTRE | wx.STAY_ON_TOP
        else:
            message = operation + " " + self.selected_card + " failed!\n" + "    Detailed Reason: " + info
            style = wx.OK | wx.ICON_ERROR | wx.CENTRE | wx.STAY_ON_TOP

        self.ShowDialog(message, style)
        logging.info(str(message))

    def GetAttr(self, card = None):
        color = "GREY"
        if card:
            state_type = card.GetStates().Type()
            color = self.colorMap[state_type]
        
        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(color)
        attr.SetReadOnly(True)
        attr.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        """SetAlignment(self, hAlign, vAlign)
        SetBackgroundColour(self, colBack)
        SetDefAttr(self, defAttr)
        SetEditor(self, editor)
        SetFont(self, font)
        SetKind(self, kind)
        SetOverflow(self, allow)
        SetReadOnly(self, isReadOnly)

        SetSize(self, num_rows, num_cols)
        SetTextColour(self, colText)"""
        attr.IncRef()
        return attr
    
    def Refresh(self, content, ignoreUninst):
        if self.content == content and self.ignoreUninst == ignoreUninst:
            return
        
        self.content = content
        self.ignoreUninst = ignoreUninst
        if not self.content or self.content.IsEmpty():
            self.CleanData()
        else:
            self.SetData(self.content)

    def AppendOneRow(self, card):
        if self.ignoreUninst and card.GetStates().Type() == data_types.STATE_TYPE_UNINST:
            return
            
        row_index = self.GetNumberRows()
        self.AppendRows(1, True)
        
        self.SetRowLabelValue(row_index, card.GetName())
        self.SetRowAttr(row_index, self.GetAttr(card))
        
        for col_index in range(self.colCount):
            value = card.GetState(self.states[col_index])
            self.SetCellValue(row_index, col_index, value)
            
    def SetData(self, content):
        self.DeleteAllRows()
        for card in content:
            self.AppendOneRow(card)

    def CleanData(self):
        for row in range(self.GetNumberRows()):
            self.SetRowAttr(row, self.GetAttr())
            for col in range(self.GetNumberCols()):
                self.SetCellValue(row, col, "-")
    
    
    def DeleteAllRows(self):
        if self.GetNumberRows():
            self.DeleteRows(0, self.GetNumberRows())
            

class ControlPanel(wx.Panel):
    
    def __init__(self, parent, configurator, id = -1, pos = wx.DefaultPosition, size = wx.DefaultSize):
        wx.Panel.__init__(self, parent, id, pos, size)
        self.configurator = configurator#configurator.Configurator("setting")
        
        self.InitUI()
        self.InitConfiguration()
        
    def InitUI(self):
        self.rdBox = wx.RadioBox(self, -1, "DCT Selection", wx.DefaultPosition, wx.DefaultSize, 
                                 ["DCT-0", "DCT-1"], 2, wx.RA_SPECIFY_COLS | wx.NO_BORDER)              
        
        sText = wx.StaticText(self, -1, "Interval:", wx.DefaultPosition, wx.DefaultSize)
        self.cbBox = wx.ComboBox(self, -1, "5s", wx.DefaultPosition, wx.DefaultSize, ["3s", "5s"], wx.CB_DROPDOWN)
        self.cbBox .SetEditable(False)
        self.ckBox = wx.CheckBox(self, -1, "Hide UNINST Card")
        
        box_sizer1 = wx.StaticBoxSizer(wx.StaticBox(self, -1, ""), wx.HORIZONTAL)
        box_sizer1.Add(sText, 0, wx.ALIGN_CENTER|wx.ALL, 2)
        box_sizer1.Add(self.cbBox, 0, wx.ALIGN_CENTER|wx.ALL, 2)
        
        box_sizer2 = wx.StaticBoxSizer(wx.StaticBox(self, -1, ""), wx.HORIZONTAL)
        box_sizer2.Add(self.ckBox, 0, wx.ALIGN_CENTER|wx.ALL, 4)

        big_sizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, ""), wx.HORIZONTAL)
        big_sizer.Add(self.rdBox, 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 35)
        big_sizer.Add(box_sizer1,  0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 35)
        big_sizer.Add(box_sizer2, 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 35)
        self.SetSizer(big_sizer)
        big_sizer.Fit(self)
        
        self.Bind(wx.EVT_RADIOBOX, self.OnTargetChanged, self.rdBox)
        self.Bind(wx.EVT_CHECKBOX, self.OnIgnoreChanged, self.ckBox)
        self.Bind(wx.EVT_COMBOBOX, self.OnIntervalChanged, self.cbBox)

        #self.Bind(wx.EVT_
    def OnTargetChanged(self, event):
        self.UpdateConfiguration()
        
    def OnIgnoreChanged(self, event):
        self.UpdateConfiguration()
        
    def OnIntervalChanged(self, event):
        self.UpdateConfiguration()
        
    def InitConfiguration(self):
        if not self.configurator:
            return False

        (self.target_ip, self.collect_interval, self.ignore_uninst) = self.configurator.Get()
        
        if self.target_ip == TARGET_IP_DCT0:
            self.rdBox.SetSelection(0)
        else:
            self.rdBox.SetSelection(1)
        
        self.cbBox.SetStringSelection(str(self.collect_interval) + "s")
        self.ckBox.SetValue(self.ignore_uninst)
        return True
            
    def UpdateConfiguration(self): 
        if not self.configurator:
            return False
            
        if self.rdBox.GetSelection() == 0:
            target = TARGET_IP_DCT0
        else:
            target = TARGET_IP_DCT1

        interval = int(str(self.cbBox.GetValue())[0])
        ignore = self.ckBox.IsChecked()

        updated = False
        if target != self.target_ip:
            self.target_ip = target
            updated = True
        if interval != self.collect_interval:
            self.collect_interval = interval
            updated = True
        if ignore != self.ignore_uninst:
            self.ignore_uninst = ignore
            updated = True
            
        if updated:
            self.configurator.Set((self.target_ip, self.collect_interval, self.ignore_uninst))

        return True
        
        
class DisplayPanel(wx.Panel):
    def __init__(self, parent, configurator, id = -1, pos = wx.DefaultPosition, size = wx.DefaultSize):
        wx.Panel.__init__(self, parent, id, pos, size)
        self.configurator = configurator
        self.grid = CardStateGrid(self)

        #sizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, ""), wx.HORIZONTAL)
        sizer.Add(self.grid, -1, wx.EXPAND|wx.ALL, 2)
        self.SetSizer(sizer)
        
    def Display(self, cardList):
        ignoreUninst = False
        if self.configurator:
            ignoreUninst = self.configurator.ShouldIgnoreUninst()
        
        self.grid.Refresh(cardList, ignoreUninst)