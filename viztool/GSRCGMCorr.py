# -*- coding: utf-8 -*-
#=================================================
# Code
#=================================================
# Thanks to Aditya and Subrai for providing this code from the previous work on the project!
# Enthought library imports
from traits.api import HasTraits, Int, Instance
from traits.api import *
from traitsui.api import Item, View, Group, HGroup, VGroup
from enable.api import Component
from enable.component_editor import ComponentEditor
from traitsui.menu import OKButton, CancelButton
# Chaco imports
from chaco.tools.api import RangeSelection, RangeSelectionOverlay
from chaco.chaco_plot_editor import ChacoPlotEditor, ChacoPlotItem
from chaco.api import Plot, ArrayPlotData, OverlayPlotContainer, create_line_plot, create_scatter_plot, add_default_axes, add_default_grids, PlotAxis, PlotLabel
from chaco.tools.api import PanTool, BroadcasterTool, ZoomTool
# Numpy imports
from numpy import *
from decimal import *
from scipy.stats import *
from read import plotallcol as plotData

def main():
    # normally this function gets its values out of other files
    x1 = 0
    x2 = 15000
    y1 = -10
    y2 = 4

     
    
    
    uebergabe = {"xlim":[x1,x2], "ylim":[y1,y2], "ranges":[x1,x2]}
    return uebergabe


class Trait(HasTraits):
    plot = Instance(Component)    

    #creates the container
    container = OverlayPlotContainer(padding = 50, fill_padding = True,
                        bgcolor = "lightgray", use_backbuffer=True)
    container2 = OverlayPlotContainer(padding = 50, fill_padding = True,
                        bgcolor = "lightgray", use_backbuffer=True)

   
    a1 = []
    b1 = []
    a2 = []
    b2 = []
    
       

    # Traits
    xmin = Float
    xmax = Float
    ymin = Float
    ymax = Float
    rangeXMin = Float
    rangeXMax = Float

    sl=plotData()
    arr,index=sl.reader("~/cyborg-t1dm/cyborg-t1dm/viztool/MYFILE104.no_gaps.csv")
    x,y =  arr['8SkinTempAve'], arr['28SensorValue']

    for i in range(len(x)):
        if x[i]!= float('inf'):      
            a1.append(x[i])
            b1.append(y[i])
        
       
    
    print len(arr['8SkinTempAve'])
    print len(a1)
    timestamp = []
    timestamp.extend(range(0,len(arr['8SkinTempAve']+1)))


    space,startpoint,maxcount=sl.bestspace(arr,index,8,90)

    space  = 115
    c,d = sl.plotter(arr,index,8,space,startpoint,90)

    print space

    mean1 = mean(a1)
    mean2 = mean(b1)
    
    std1 = std(a1)
    std2 = std(b1)

    for i in range(len(x)):
        if x[i]!= float('inf'):
            a2.append((x[i]-mean1)/std1)
            b2.append((y[i]-mean2)/std2)
            
        else:
            a2.append(-1)
            b2.append(-1)

    print len(a2) 
    z = [0]*space
    e = z+b2
    
    

    
    '''
    mean1 = mean(x)
    mean2 = mean(y)

    print mean1
    print mean2
    
    std1 = std(x)
    std2 = std(y)

    for i in range(len(x)):
        a.append((x[i] - mean1)/std1)
        b.append((y[i] - mean2)/std2)

    
    z = [0]*space
    e = z+a
     
    #print e
    '''
    # TraitsUI view
    traits_view = View(Group(
        HGroup(
            VGroup(Item("container", editor = ComponentEditor(), show_label = False)),
            VGroup(Item("container2", editor = ComponentEditor(), show_label = False))),        
        HGroup(Item("xmin"), Item("xmax"), Item("ymin"), Item("ymax"), show_border = True, label = "Plotborders"),
        HGroup(Item("rangeXMin", label="x_min"), Item("rangeXMax", label="x_max"), show_border = True, label="Range of right plot")), 
        buttons = [OKButton, CancelButton], resizable = True, width = 1000, height = 500)

    # Constructor
    def __init__(self):
        super(Trait, self).__init__()

        uebergabe = main()

        # initialize traits
        self.xmin = uebergabe["xlim"][0]
        self.xmax = uebergabe["xlim"][1]
        self.ymin = uebergabe["ylim"][0]
        self.ymax = uebergabe["ylim"][1]
        self.rangeXMin = uebergabe["ranges"][0]
        self.rangeXMin = uebergabe["ranges"][1]

        self.y3 = 0
        self.y4 = 1


        self._create_Container()


    def _create_Container(self):

        #creating dict of plots and the broadcaster
        plots = {}
        broadcaster = BroadcasterTool()

        #=====================first container===========================

        #first plot
        #index = linspace(-2*pi,2*pi,1000)
        plot = create_line_plot((self.timestamp, self.e), color = "black", index_bounds=(self.xmin, self.xmax), value_bounds = (self.ymin, self.ymax))
        plot.bgcolor = "white"
        plot.border_visible = True
        value_mapper = plot.value_mapper
        index_mapper = plot.index_mapper
        add_default_grids(plot)
        add_default_axes(plot)

        self.sync_trait("xmin", index_mapper.range, "_low_value")
        self.sync_trait("xmax", index_mapper.range, "_high_value")
        self.sync_trait("ymin", value_mapper.range, "_low_value")
        self.sync_trait("ymax", value_mapper.range, "_high_value")
        
       
        # range selection
        self.rangeselect = RangeSelection(plot, left_button_selects = False, auto_handle_event = False)
        plot.active_tool = self.rangeselect
        plot.overlays.append(RangeSelectionOverlay(component=plot))
        self.rangeselect.on_trait_change(self.on_selection_changed, "selection")

        #adds plot to the container
        self.container.add(plot)

        # second plot
        index2 = linspace(-5*pi,4*pi,1000)
        plot = create_line_plot((self.timestamp, self.a2), color = "red", index_bounds=(self.xmin, self.xmax), value_bounds = (self.ymin, self.ymax))
        print plot
        plot.value_mapper = value_mapper
        value_mapper.range.add(plot.value)
        plot.index_mapper = index_mapper
        index_mapper.range.add(plot.index)

        # Create a pan tool and give it a reference to the plot
        pan = PanTool(plot, drag_button="left")
        broadcaster.tools.append(pan)

        # allows to zoom
        zoom = ZoomTool(plot, tool_mode="box", always_on = False, visible = True)
        plot.overlays.append(zoom)


        #adds plot to the container
        self.container.add(plot)

        # appends broadcaster to the container
        self.container.tools.append(broadcaster)

        # title of the container
        self.container.overlays.append(PlotLabel("Plotting of the Normalized SkinTemp and CGM Timeseries ", component=self.container, overlay_position = "top"))

        #==============end of first container===========================

        #====================second container===========================

        #first plot2
        
        plot2 = create_line_plot((self.c, self.d), color = "blue", index_bounds=(self.rangeXMin, self.rangeXMax), value_bounds = (self.y3, self.y4))
        plot2.bgcolor = "white"
        plot2.border_visible = True
        #plot2.value_mapper = value_mapper # the plot uses the same index and
        #plot2.index_mapper = index_mapper # value like the plots of container1
        self.sync_trait("rangeXMin", plot2.index_mapper.range, "low", False)
        self.sync_trait("rangeXMax", plot2.index_mapper.range, "high", False)


        plot2.index_mapper.range.low = 0
        plot2.index_mapper.range.high = 10000

        plot2.value_mapper.range.low = 0
        plot2.value_mapper.range.high = 1
    
        value_mapper.range.add(plot2.value)
        index_mapper.range.add(plot2.index)
        add_default_grids(plot2)
        add_default_axes(plot2)

        #adds plot to the container
        self.container2.add(plot2)

        # title of the container
        self.container2.overlays.append(PlotLabel("R-Squared Correlation", component=self.container, overlay_position = "top"))

        index_mapper.on_trait_change(self.on_mapper_updated, "updated")

        #=============end of second container===========================

    def on_mapper_updated(self, mapper, name, value):
        if not self.rangeselect.selection:
            self.rangeXMin = mapper.range.low
            self.rangeXMax = mapper.range.high
           
    def on_selection_changed(self, selection):
        if selection != None:
            self.rangeXMin, self.rangeXMax = selection
            #print selection
            print pearsonr (self.x,self.y)

gui = Trait()
gui.configure_traits()
