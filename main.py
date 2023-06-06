import datasource
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
from tkinter.simpledialog import askinteger, askstring
from messageWindow import MapDisplay
from tkinter import messagebox
import time
sbi_numbers = 3
bemp_numbers = 3
sna_string = ''
ar_string = ''


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        # add menubar that contains a menu
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        self.keyword = ""

        
        image=Image.open("./test_images/setting.png")
        resize_img=image.resize((20,20))
        self.icons = ImageTk.PhotoImage(resize_img)
       
        # exit image
        image2=Image.open("./test_images/exit.png")
        resize_img2=image2.resize((20,20))
        self.icons2= ImageTk.PhotoImage(resize_img2)
        # mirror image
        image3=Image.open("./test_images/mirror.png")
        resize_img3=image3.resize((20,20))
        self.icons3= ImageTk.PhotoImage(resize_img3)
        # book image
        image4=Image.open("./test_images/book.png")
        resize_img4=image4.resize((20,20))
        self.icons4= ImageTk.PhotoImage(resize_img4)
        
        # add command menu in menubar   

        self.command_menu = tk.Menu(self.menubar)
        self.search_menu = tk.Menu()
        self.explain_menu=tk.Menu()
        self.menubar.add_cascade(label="File", menu=self.command_menu)
        self.command_menu.add_command(
            label="設定", command=self.menu_setting_click,image=self.icons,compound='left')
        self.command_menu.add_command(label="離開", command=self.destroy,image=self.icons2,compound='left')
        self.menubar.add_cascade(label="搜尋", menu=self.search_menu)
        self.search_menu.add_command(
            label="站點搜尋", command=self.site_search_click,image=self.icons3,compound='left')
        self.menubar.add_cascade(label="說明", menu=self.explain_menu)
        self.explain_menu.add_command(label="說明",command=self.explain,image=self.icons4,compound='left')
        # main Frame
        mainFrame = ttk.Frame(self)
        updateButton = tk.Button(mainFrame,text="立即更新",bg="gray",fg="gold",font=('italic',16),relief='groove',activebackground='skyblue',activeforeground='green',command=lambda :datasource.getInfo())
        updateButton.pack(pady=(20,0))
        # self.style = ttk.Style(self)
        # self.style.theme_use('classic')
        # self.style.configure('.', font='Helvetica 13', foreground='#D2691E', background='#F0F8FF')
        localtime = time.localtime()
        self.updateDate = time.strftime("%Y-%m-%d", localtime)
        self.updateDateLabel = tk.Label(mainFrame, text="更新日期:"+self.updateDate,font=("Courier", 12),fg="green")
        self.updateDateLabel.pack(pady=(10,0))
        mainFrame.pack(padx=50, pady=80)
       
        # logoLabel top of top_wrapperFrame
        logoImage = Image.open('./test_images/logo2.png')
        resizeImage = logoImage.resize((270, 68), Image.LANCZOS)
        self.logoTkimage = ImageTk.PhotoImage(resizeImage)
        logoLabel = ttk.Label(mainFrame, image=self.logoTkimage)
        logoLabel.pack(pady=(0, 50))
        
        # logoLabel top of top_wrapperFrame
        logoLabel = ttk.Label
        # top_wrapperFrame=================
        top_wrapperFrame = ttk.Frame(mainFrame)
        
        top_wrapperFrame.pack(fill=tk.X)

        # topFrame_start===================
        topFrame = ttk.LabelFrame(top_wrapperFrame, text="台北市行政區")
        length = len(datasource.sarea_list)
        self.radioStringVar = tk.StringVar()
        for i in range(length):
            cols = i % 3
            rows = i // 3
            ttk.Radiobutton(topFrame, text=datasource.sarea_list[i], value=datasource.sarea_list[i], variable=self.radioStringVar, command=self.radio_Event).grid(
                column=cols, row=rows, sticky=tk.W, padx=10, pady=10)

        topFrame.pack(side=tk.LEFT)
        self.radioStringVar.set('信義區')
        self.area_data = datasource.getInfoFromArea('信義區')
        # topFrame_end=====================

        # sbi_warningFrame_start====================
        self.sbi_warningFrame = ttk.LabelFrame(top_wrapperFrame)
        columns = ('#1', '#2', '#3')
        self.sbi_tree = ttk.Treeview(
            self.sbi_warningFrame, columns=columns, show='headings')
        self.sbi_tree.heading('#1', text='站點')
        self.sbi_tree.column("#1", minwidth=0, width=200)
        self.sbi_tree.heading('#2', text='可借')
        self.sbi_tree.column("#2", minwidth=0, width=30)
        self.sbi_tree.heading('#3', text='可還')
        self.sbi_tree.column("#3", minwidth=0, width=30)
        self.sbi_tree.pack(side=tk.LEFT)
        self.sbi_warning_data = datasource.filter_sbi_warning_data(
            self.area_data, sbi_numbers)
        sbi_sites_numbers = len(self.sbi_warning_data)
        print(sbi_sites_numbers)
        self.sbi_warningFrame.configure(text=f"可借不足站點數:{sbi_sites_numbers}")
        for item in self.sbi_warning_data:
            self.sbi_tree.insert('', tk.END, values=[
                                 item['sna'][11:], item['sbi'], item['bemp']])
        self.sbi_warningFrame.pack(side=tk.LEFT)
        # sbi_warningFrame_end======================

        # bemp_warningFrame_start====================
        self.bemp_warningFrame = ttk.LabelFrame(
            top_wrapperFrame, text="可還目前不足站點")
        columns = ('#1', '#2', '#3')
        self.bemp_tree = ttk.Treeview(
            self.bemp_warningFrame, columns=columns, show='headings')
        self.bemp_tree.heading('#1', text='站點')
        self.bemp_tree.column("#1", minwidth=0, width=200)
        self.bemp_tree.heading('#2', text='已借')
        self.bemp_tree.column("#2", minwidth=0, width=30)
        self.bemp_tree.heading('#3', text='可還')
        self.bemp_tree.column("#3", minwidth=0, width=30)
        self.bemp_tree.pack(side=tk.LEFT)
        self.bemp_warning_data = datasource.filter_bemp_warning_data(
            self.area_data, bemp_numbers)
        bemp_sites_numbers = len(self.bemp_warning_data)
        self.bemp_warningFrame.configure(text=f"可還不足站點數:{bemp_sites_numbers}")
        for item in self.bemp_warning_data:
            self.bemp_tree.insert('', tk.END, values=[
                                  item['sna'][11:], item['sbi'], item['bemp']])
        self.bemp_warningFrame.pack(side=tk.LEFT)
        # bemp_warningFrame_end======================
        # get current datetime
        now = datetime.datetime.now()
        # display current datetime
        nowString = now.strftime("%Y-%m-%d %H:%M:%S")
        self.bottomFrame = ttk.LabelFrame(self, text=f"信義區-{nowString}")
        self.bottomFrame.pack()

        columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7')
        self.tree = ttk.Treeview(
            self.bottomFrame, columns=columns, show='headings')
        self.tree.heading('#1', text='站點')
        self.tree.column("#1", minwidth=0, width=200)
        self.tree.heading('#2', text='時間')
        self.tree.column("#2", minwidth=0, width=200)
        self.tree.heading('#3', text='總車數')
        self.tree.column("#3", minwidth=0, width=50)
        self.tree.heading('#4', text='可借')
        self.tree.column("#4", minwidth=0, width=30)
        self.tree.heading('#5', text='可還')
        self.tree.column("#5", minwidth=0, width=30)
        self.tree.heading('#6', text='地址')
        self.tree.column("#6", minwidth=0, width=250)
        self.tree.heading('#7', text='狀態')
        self.tree.column("#7", minwidth=0, width=30)
        self.tree.pack(side=tk.LEFT)
        # self.tree,addItem
        for item in self.area_data:
            self.tree.insert('', tk.END, values=[
                item['sna'][11:], item['mday'], item['tot'], item['sbi'], item['bemp'], item['ar'], item['act']], tags=item['sna'])

        # self.tree bind event
        self.tree.bind('<<TreeviewSelect>>', self.treeSelected)

        # 幫treeview加scrollbar------------------------------------------------
        scrollbar = ttk.Scrollbar(self.bottomFrame, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)

        bemp_scrollbar = ttk.Scrollbar(
            self.bemp_warningFrame, command=self.bemp_tree.yview)
        bemp_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.bemp_tree.config(yscrollcommand=bemp_scrollbar.set)

        sbi_scrollbar = ttk.Scrollbar(
            self.sbi_warningFrame, command=self.sbi_tree.yview)
        sbi_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sbi_tree.config(yscrollcommand=sbi_scrollbar.set)

    '''
    self.tree.bind('<ButtonRelease-1>',self.sortby)

    def sortby(self,event):
        col = self.tree.identify_column(event.x)
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        items.sort(reverse=True)
        for index, (val, k) in enumerate(items):
            self.tree.move(k, '', index)
        self.tree.heading(col, command=lambda: self.sortby(col, 0))
    '''
        
    def treeSelected(self, event):
        selectedTree = event.widget
        # if len(selectedTree.selection())==0:return
        itemTag = selectedTree.selection()[0]
        itemDic = (selectedTree.item(itemTag))
        sitename = itemDic['tags'][0]
        for item in self.area_data:
            if sitename == item['sna']:
                selected_data = (item)
                break
        # 顯示地圖的display
        mapDisplay = MapDisplay(self, selected_data)

    def menu_setting_click(self):
        global sbi_numbers, bemp_numbers
        retVal = askinteger(f"目前設定不足數量:{sbi_numbers}",
                            "請輸入不足可借可還數量0~5",
                            minvalue=0, maxvalue=5)
        print(retVal)
        sbi_numbers = retVal
        bemp_numbers = retVal
    # THIS METHOD DISPLAY THE SITE NAME RESULT

    def site_search_click(self):
        keyword = askstring("站點搜尋", f"目前關鍵字:{self.keyword}\n輸入新的關鍵字:")
        print(f"siteVal = {keyword}")
        if not (keyword == None):
            self.keyword = keyword
            self.refresh()

    def radio_Event(self):
        self.refresh()
       
    def refresh(self):
        # get current datetime
        now = datetime.datetime.now()
        # display current datetime
        nowString = now.strftime("%Y-%m-%d %H:%M:%S")

        # Clear tree view
        for item in self.tree.get_children():
            self.tree.delete(item)

        for item in self.sbi_tree.get_children():
            self.sbi_tree.delete(item)

        for item in self.bemp_tree.get_children():
            self.bemp_tree.delete(item)

        # Get selected radio button value
        area_name = self.radioStringVar.get()

        self.bottomFrame.config(text=f"{area_name}-{nowString}")

        # Get all station data from selected area
        self.area_data = datasource.getInfoFromArea(area_name, keyword=self.keyword)

        # Filter data with sbi warning number
        self.sbi_warning_data = datasource.filter_sbi_warning_data(
            self.area_data, sbi_numbers)
        sbi_site_numbers = len(self.sbi_warning_data)
        self.sbi_warningFrame.config(text=f"可借不足站點數:{sbi_site_numbers}")

        # Filter data with bemp warning number
        self.bemp_warning_data = datasource.filter_bemp_warning_data(
            self.area_data, bemp_numbers)
        bemp_site_numbers = len(self.bemp_warning_data)
        self.bemp_warningFrame.configure(text=f"可還不足站點數:{bemp_site_numbers}")

        # Display data in tree view
        for item in self.area_data:
            self.tree.insert('', tk.END, values=[
                             item['sna'][11:], item['mday'], item['tot'], item['sbi'], item['bemp'], item['ar'], item['act']], tags=item['sna'])

        for item in self.sbi_warning_data:
            self.sbi_tree.insert('', tk.END, values=[
                                 item['sna'][11:], item['sbi'], item['bemp']])

        for item in self.bemp_warning_data:
            self.bemp_tree.insert('', tk.END, values=[
                                  item['sna'][11:], item['sbi'], item['bemp']])
    def explain(self):
       messagebox.showinfo("YOUBIKE", "這是python11202應用實戰班23號的期末專題")
    
def main():
    window = Window()
    window.title("台北市youbike2.0資訊",)
    window.mainloop()


if __name__ == "__main__":
    main()
