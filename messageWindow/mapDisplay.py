import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog
import tkintermapview as tkmap
import tkinter

class MapDisplay(Dialog):
    def __init__(self, master, data_dict, **kwargs):
        self.site_info = data_dict
        self.current_map_mode = 'google_normal'  # 初始化為Google普通地圖模式
        super().__init__(master, **kwargs)

    def body(self, master):
        
        
        self.search_bar = ttk.Entry(master=self, width=130)
        self.search_bar.pack(side=tk.TOP)
        # self.search_bar.focus()

        self.search_bar_button = ttk.Button(master=self, width=8, text="搜尋", command=self.search)
        self.search_bar_button.pack(side=tk.TOP)
        

        self.search_bar_clear = ttk.Button(master=self, width=8, text="清除", command=self.clear)
        self.search_bar_clear.pack(side=tk.TOP)
        
        self.map_widget = tkmap.TkinterMapView(
            self, width=800, height=600, corner_radius=0)
        self.map_widget.pack()

        marker_1 = self.map_widget.set_position(
            self.site_info['lat'], self.site_info['lng'], marker=True)  # 台北市位置
        # marker_1.set_text("台北市中心")
        self.map_widget.set_zoom(20)  # 設定顯示大小
        marker_1.set_text(self.site_info['sna'][11:])
        self.set_map_mode('google_normal')  # 設定初始地圖模式

    def buttonbox(self):
        boxFrame = tk.Frame(self)
        

        close_button = ttk.Button(boxFrame, text="關閉", command=self.on_closing)
        close_button.pack(side=tk.RIGHT, padx=340)
        # self.bind("<Return>", self.ok)

        switch_mode_button = ttk.Button(
            boxFrame, text="地圖模式", width=15, command=self.switch_map_mode)
        switch_mode_button.pack(side=tk.RIGHT)
        
        self.marker_list_box = tkinter.Listbox(self, height=8,width=20)
        self.marker_list_box.config(width=100, height=4)
        self.marker_list_box.pack(padx=10, pady=10)
        # self.listbox_button_frame = tkinter.Frame(master=self)
        # self.listbox_button_frame.pack()
        self.save_marker_button = ttk.Button(master=boxFrame, width=20, text="記憶標記",command=self.save_marker)
        self.save_marker_button.pack(side=tk.LEFT)
        
        self.clear_marker_button = ttk.Button(master=self, width=20, text="清除標記",
                                                  command=self.clear_marker_list)
        self.clear_marker_button.pack(side=tk.LEFT)
        
        
        self.connect_marker_button = ttk.Button(master=boxFrame, width=20, text="路線",
                                                    command=self.connect_marker)
        self.connect_marker_button.pack(side=tk.LEFT)

        self.marker_list = []
        self.marker_path = None

        self.search_marker = None
        self.search_in_progress = False
        
        boxFrame.pack()

    def set_map_mode(self, mode):
        if mode == 'google_normal':
            self.map_widget.set_tile_server(
                "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif mode == 'google_satellite':
            self.map_widget.set_tile_server(
                "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif mode == 'open_street_map':
            self.map_widget.set_tile_server(
                "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=22)
        # elif mode == 'water_color_map':
        #     self.map_widget.set_tile_server(
        #         "http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.png", max_zoom=22)
        elif mode =='black_and_white_map':
            self.map_widget.set_tile_server(
                "http://a.tile.stamen.com/toner/{z}/{x}/{y}.png",max_zoom=22)
        # elif mode =='detailed_hiking_map':
        #     self.map_widget.set_tile_server(
        #         "https://tiles.wmflabs.org/hikebike/{z}/{x}/{y}.png",max_zoom=22)
        # elif mode =='no_label_map':
        #     self.map_widget.set_tile_server(
        #         "https://tiles.wmflabs.org/osm-no-labels/{z}/{x}/{y}.png",max_zoom=22)
        # elif mode =='swisstopo_map':
        #     self.map_widget.set_tile_server(
        #         "https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/{z}/{x}/{y}.jpeg",max_zoom=22)
        # else:
        #     raise ValueError(f'Invalid map mode: {mode}')

        self.current_map_mode = mode

    def switch_map_mode(self):
        if self.current_map_mode == 'google_normal':
            self.set_map_mode('google_satellite')
        elif self.current_map_mode == 'google_satellite':
            self.set_map_mode('open_street_map')
        # elif self.current_map_mode =='open_street_map':
        #     self.set_map_mode('water_color_map')
        elif self.current_map_mode =='open_street_map':
            self.set_map_mode('black_and_white_map')
        # elif self.current_map_mode =='black_and_white_map':
        #     self.set_map_mode('detailed_hiking_map')
        # elif self.current_map_mode =='detailed_hiking_map':
        #     self.set_map_mode('no_label_map')
        # elif self.current_map_mode =='no_label_map':
        #     self.set_map_mode('swisstopo_map')
        else:
            self.set_map_mode('google_normal')
    
    
    
    def search(self, event=None):
        if not self.search_in_progress:
            self.search_in_progress = True
            if self.search_marker not in self.marker_list:
                self.map_widget.delete(self.search_marker)

            address = self.search_bar.get()
            self.search_marker = self.map_widget.set_address(address, marker=True)
            if self.search_marker is False:
                # address was invalid (return value is False)
                self.search_marker = None
            self.search_in_progress = False
    
    def save_marker(self):
        if self.search_marker is not None:
            self.marker_list_box.insert(tkinter.END, f" {len(self.marker_list)}. {self.search_marker.text} ")
            self.marker_list_box.see(tkinter.END)
            self.marker_list.append(self.search_marker)
    
    def clear_marker_list(self):
        for marker in self.marker_list:
            self.map_widget.delete(marker)

        self.marker_list_box.delete(0, tkinter.END)
        self.marker_list.clear()
        self.connect_marker()

    def connect_marker(self):
        print(self.marker_list)
        position_list = []

        for marker in self.marker_list:
            position_list.append(marker.position)

        if self.marker_path is not None:
            self.map_widget.delete(self.marker_path)

        if len(position_list) > 0:
            self.marker_path = self.map_widget.set_path(position_list)

    def clear(self):
        self.search_bar.delete(0, last=tkinter.END)
        self.map_widget.delete(self.search_marker)


    def on_closing(self, event=0):
        self.destroy()
        exit()