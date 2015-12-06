# -*- coding: utf-8 -*-


import os
import logging
from PyQt5 import QtWidgets, QtCore, QtGui, uic, QtSvg
from widgets import widgets
from .marker import PipValueMarkerBase



class PlayerMarker(PipValueMarkerBase):
    signalPlayerPositionUpdate = QtCore.pyqtSignal(float, float, float)
    
    def __init__(self, widget, imageFactory, color, parent = None):
        super().__init__(widget.mapScene, widget.mapView, parent)
        self.markerType = 0
        self.widget = widget
        self.imageFactory = imageFactory
        self.imageFilePath = os.path.join('res', 'mapmarkerplayer.svg')
        self.pipValueListenerDepth = 1
        self.markerItem.setZValue(10)
        self.setColor(color,False)
        self.setLabelFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold), False)
        self.setLabel('Player', False)
        self.doUpdate()
        
    def _getPixmap_(self):
        return self.imageFactory.getPixmap(self.imageFilePath, size=32, color=self.color)
    
    @QtCore.pyqtSlot()        
    def _slotPipValueUpdated(self):
        self.setVisible(True)
        rx = self.pipValue.child('X').value()
        ry = self.pipValue.child('Y').value()
        px = self.mapCoords.pip2map_x(rx)
        py = self.mapCoords.pip2map_y(ry)
        pr = self.pipValue.child('Rotation').value()
        self.markerItem.setToolTip( 'Pos: (' + str(rx) + ', ' + str(ry) + ')\n'
                                + 'Rot: ' + str(pr))
        self.setMapPos(px, py, pr)
        self.signalPlayerPositionUpdate.emit(px, py, pr)


class CustomMarker(PipValueMarkerBase):
    def __init__(self, widget, imageFactory, color, parent = None):
        super().__init__(widget.mapScene, widget.mapView, parent)
        self.markerType = 1
        self.widget = widget
        self.imageFactory = imageFactory
        self.imageFilePath = os.path.join('res', 'mapmarkercustom.svg')
        self.pipValueListenerDepth = 1
        self.markerItem.setZValue(0)
        self.setColor(color,False)
        self.setLabelFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold), False)
        self.setLabel('Custom Marker', False)
        self.doUpdate()
        
    def _getPixmap_(self):
        return self.imageFactory.getPixmap(self.imageFilePath, size=48, color=self.color)
            
    def _updateMarkerOffset_(self):
        mb = self.markerItem.boundingRect()
        self.markerItem.setOffset(-mb.width()/2, -mb.height())
    
    @QtCore.pyqtSlot()        
    def _slotPipValueUpdated(self):
        isVisible = self.pipValue.child('Visible').value()
        if isVisible:
            self.setVisible(True)
            rx = self.pipValue.child('X').value()
            ry = self.pipValue.child('Y').value()
            px = self.mapCoords.pip2map_x(rx)
            py = self.mapCoords.pip2map_y(ry)
            height = self.pipValue.child('Height').value()
            self.markerItem.setToolTip( 'Pos: (' + str(rx) + ', ' + str(ry) + ')\n'
                                        + 'Visible: ' + str(isVisible) + '\n'
                                        + 'Height: ' +str(height) )
            self.setMapPos(px, py)
        else:
            self.setVisible(False)
        
    def _fillMarkerContextMenu_(self, event, menu):
        if self.pipValue:
            @QtCore.pyqtSlot()
            def _removeCustomMarker():
                self.datamanager.rpcRemoveCustomMarker()
            menu.addAction('Remove Marker', _removeCustomMarker)
    
    
class PowerArmorMarker(PipValueMarkerBase):
    def __init__(self, widget, imageFactory, color, parent = None):
        super().__init__(widget.mapScene, widget.mapView, parent)
        self.markerType = 2
        self.widget = widget
        self.imageFactory = imageFactory
        self.imageFilePath = os.path.join('res', 'mapmarkerpowerarmor.svg')
        self.pipValueListenerDepth = 1
        self.markerItem.setZValue(0)
        self.setColor(color,False)
        self.setLabelFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold), False)
        self.setLabel('Power Armor', False)
        self.filterVisibleFlag = True
        self.PipVisible = False
        self.doUpdate()
        
    def _getPixmap_(self):
        return self.imageFactory.getPixmap(self.imageFilePath, size=32, color=self.color)
    
    @QtCore.pyqtSlot(bool)
    def filterSetVisible(self, value):
        self.filterVisibleFlag = value
        if not value:
            self.setVisible(False)
        elif value and self.PipVisible:
            self.setVisible(True)
            self.doUpdate()
    
    @QtCore.pyqtSlot()        
    def _slotPipValueUpdated(self):
        self.PipVisible = self.pipValue.child('Visible').value()
        rx = self.pipValue.child('X').value()
        ry = self.pipValue.child('Y').value()
        px = self.mapCoords.pip2map_x(rx)
        py = self.mapCoords.pip2map_y(ry)
        height = self.pipValue.child('Height').value()
        self.markerItem.setToolTip( 'Pos: (' + str(rx) + ', ' + str(ry) + ')\n'
                                    + 'Visible: ' + str(self.PipVisible) + '\n'
                                    + 'Height: ' +str(height) )
        self.setMapPos(px, py, False)
        if self.PipVisible and self.filterVisibleFlag:
            self.setVisible(True)
            self.doUpdate()
        else:
            self.setVisible(False)
    


class QuestMarker(PipValueMarkerBase):
    def __init__(self, widget, imageFactory, color, parent = None):
        super().__init__(widget.mapScene, widget.mapView, parent)
        self.markerType = 3
        self.widget = widget
        self.imageFactory = imageFactory
        self.imageFilePath = os.path.join('res', 'mapmarkerquest.svg')
        self.pipValueListenerDepth = 1
        self.markerItem.setZValue(0)
        self.setColor(color,False)
        self.setLabelFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold), False)
        self.setLabel('Quest Marker', False)
        self.doUpdate()
        
    def _getPixmap_(self):
        return self.imageFactory.getPixmap(self.imageFilePath, size=32, color=self.color)
            
    def _updateMarkerOffset_(self):
        mb = self.markerItem.boundingRect()
        self.markerItem.setOffset(-mb.width()/2, -mb.height())
        
    @QtCore.pyqtSlot()        
    def _slotPipValueUpdated(self):
        self.setVisible(True)
        name = self.pipValue.child('Name').value()
        self.setLabel(name, False)
        rx = self.pipValue.child('X').value()
        ry = self.pipValue.child('Y').value()
        px = self.mapCoords.pip2map_x(rx)
        py = self.mapCoords.pip2map_y(ry)
        height = self.pipValue.child('Height').value()
        tttext =  'Pos: (' + str(rx) + ', ' + str(ry) + ')\n';
        tttext += 'Height: ' +str(height)
        onDoor = self.pipValue.child('OnDoor').value()
        if onDoor != None:
            tttext += '\nOnDoor: ' + str(onDoor)
        shared = self.pipValue.child('Shared').value()
        if shared != None:
            tttext += '\nShared: ' + str(shared)
        questids = self.pipValue.child('QuestId').value()
        if questids != None:
            tttext += '\nQuestIds: ['
            isFirst = True
            for q in questids:
                if isFirst:
                    isFirst = False
                else:
                    tttext += ', '
                tttext += str(q.value())
            tttext += ']'
        self.markerItem.setToolTip( tttext )
        self.setMapPos(px, py)
        
    
class LocationMarker(PipValueMarkerBase):
    def __init__(self, widget, imageFactory, color, parent = None):
        super().__init__(widget.mapScene, widget.mapView, parent)
        self.markerType = 4
        self.widget = widget
        self.imageFactory = imageFactory
        self.pipValueListenerDepth = 1
        self.markerItem.setZValue(0)
        self.setColor(color,False)
        self.setLabelFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold), False)
        self.setLabel('Location', False)
        self.locType = -1
        self.noTypePixmapFound = False
        self.discovered = False
        self.lastKnownDiscovered = False
        self.visible = False
        self.cleared = False
        self.filterVisibleFlag = True
        self.filterVisibilityCheatFlag = False
        self.doUpdate()
        
    def _getPixmap_(self):
        def _getDefaultPixmap():
            if self.discovered:
                self.imageFilePath = os.path.join('res', 'mapmarkerloctype_default_d.svg')
            else:
                self.imageFilePath = os.path.join('res', 'mapmarkerloctype_default_u.svg')
            return self.imageFactory.getPixmap(self.imageFilePath, size=28, color=self.color)
        if self.locType < 0:
            return _getDefaultPixmap()
        else:
            filepath = 'mapmarkerloctype_' + str(self.locType)
            if self.discovered:
                self.imageFilePath = os.path.join('res', filepath + '_d.svg')
            else:
                self.imageFilePath = os.path.join('res', filepath + '_u.svg')
            p = self.imageFactory.getPixmap(self.imageFilePath, size=28, color=self.color)
            if not p:
                self.noTypePixmapFound = True
                p = _getDefaultPixmap()
            return p
    
    @QtCore.pyqtSlot(bool)
    def filterSetVisible(self, value, update = True):
        self.filterVisibleFlag = value
        if not value:
            self.setVisible(False)
        elif value and self.visible:
            self.setVisible(True)
            if update:
                self.doUpdate()
    
    @QtCore.pyqtSlot(bool)
    def filterVisibilityCheat(self, value, update = True):
        self.filterVisibilityCheatFlag = value
        if not self.visible:
            if value:
                self.setVisible(True)
                if update:
                    self.doUpdate()
            else:
                self.setVisible(False)
    
    def setPipValue(self, value, datamanager, mapCoords = None, signal = True):
        super().setPipValue(value, datamanager, mapCoords, signal)
        self.invalidateMarkerPixmap(signal)
        
    @QtCore.pyqtSlot()        
    def _slotPipValueUpdated(self):
        self.visible = self.pipValue.child('Visible').value()
        name = self.pipValue.child('Name')
        if name:
            self.setLabel(name.value(), False)
        else:
            self.setLabel('<Location>', False)
        loctype = self.pipValue.child('type')
        if loctype:
            self.locType = loctype.value()
        else:
            self.locType = -1
        discovered = self.pipValue.child('Discovered')
        if discovered:
            self.discovered = discovered.value()
        cleared = self.pipValue.child('ClearedStatus')
        if cleared:
            self.cleared = cleared.value()
        if self.discovered != self.lastKnownDiscovered:
            self.invalidateMarkerPixmap(False)
        self.lastKnownDiscovered = self.discovered
        rx = self.pipValue.child('X').value()
        ry = self.pipValue.child('Y').value()
        px = self.mapCoords.pip2map_x(rx)
        py = self.mapCoords.pip2map_y(ry)
        tttext = 'Pos: (' + str(rx) + ', ' + str(ry) + ')'
        props = self.pipValue.value()
        for prop in props:
            if prop != 'X' and prop !='Y':
                tttext += '\n' + prop + ': ' + str(props[prop].value())
        self.markerItem.setToolTip( tttext )
        if (self.visible or self.filterVisibilityCheatFlag) and self.filterVisibleFlag:
            self.setVisible(True)
            self.setMapPos(px, py)
        else:
            self.setMapPos(px, py, False)
            
    def _labelStr_(self):
        tmp = self.label
        if self.cleared:
            tmp += '\n[CLEARED]'
        if self.noTypePixmapFound:
            tmp += '\n(LocType: ' + str(self.locType) + ')'
        return tmp
        
        return self.label
        
    def _fillMarkerContextMenu_(self, event, menu):
        if self.pipValue:
            @QtCore.pyqtSlot()
            def _fastTravel():
                if QtWidgets.QMessageBox.question(self.view, 'Fast Travel', 
                        'Do you want to travel to ' + self.label + '?') == QtWidgets.QMessageBox.Yes:
                    self.datamanager.rpcFastTravel(self.pipValue)
            ftaction = menu.addAction('Fast Travel', _fastTravel)
            
    def _markerDoubleClickEvent_(self, event):
        if self.pipValue:
            if QtWidgets.QMessageBox.question(self.view, 'Fast Travel', 
                    'Do you want to travel to ' + self.label + '?') == QtWidgets.QMessageBox.Yes:
                self.datamanager.rpcFastTravel(self.pipValue)
        




class MapGraphicsItem(QtCore.QObject):
    
    MAP_NWX = 36
    MAP_NWY = 50
    MAP_NEX = 2000
    MAP_NEY = 50
    MAP_SWX = 36
    MAP_SWY = 1978
    
    class PixmapItem(QtWidgets.QGraphicsPixmapItem):
        def __init__(self, parent, qparent = None):
            super().__init__(qparent)
            self.parent = parent

    def __init__(self, gwidget, imageFactory, mapfile, color = None, colorable = True, qparent = None):
        super().__init__(qparent)
        self.gwidget = gwidget
        self.imageFactory = imageFactory
        self.mapfile = mapfile
        self.colorUpdate = color
        self.colorable = colorable
        self.mapItem = self.PixmapItem(self)
        self.gwidget.mapScene.addItem(self.mapItem)
        self.setMapPixmap(imageFactory.getPixmap(mapfile, color = color))
        self.mapItem.setZValue(-10)
            
    def setMapPixmap(self, pixmap):
        self.mapItem.setPixmap(pixmap)
        self.gwidget.mapScene.setSceneRect(self.mapItem.sceneBoundingRect())
    
    @QtCore.pyqtSlot(float, float, float)
    def setZoomLevel(self, zoom, mapposx, mapposy):
        self.mapItem.setTransform(QtGui.QTransform.fromScale(zoom, zoom))
        self.gwidget.mapScene.setSceneRect(self.mapItem.sceneBoundingRect())
        if mapposx >= 0 and mapposy >=0:
            self.gwidget.mapView.centerOn(mapposx * zoom, mapposy * zoom)
    
    @QtCore.pyqtSlot(QtGui.QColor)
    def setColor(self, color):
        self.colorUpdate = color
        self.setMapPixmap(self.imageFactory.getPixmap(self.mapfile, color = color))



class GlobalMapWidget(widgets.WidgetBase):
    
    signalSetZoomLevel = QtCore.pyqtSignal(float, float, float)
    signalSetColor = QtCore.pyqtSignal(QtGui.QColor)
    signalSetStickyLabel = QtCore.pyqtSignal(bool)
    signalLocationFilterSetVisible = QtCore.pyqtSignal(bool)
    signalLocationFilterVisibilityCheat = QtCore.pyqtSignal(bool)
    
    _signalPipWorldQuestsUpdated = QtCore.pyqtSignal()
    _signalPipWorldLocationsUpdated = QtCore.pyqtSignal()
    
    MAPZOOM_SCALE_MAX = 4.0
    MAPZOOM_SCALE_MIN = 0.1
  
    def __init__(self, handle, controller, parent):
        super().__init__('Global Map', parent)
        self.basepath = handle.basepath
        self.controller = controller
        self.widget = uic.loadUi(os.path.join(self.basepath, 'ui', 'globalmapwidget.ui'))
        self.setWidget(self.widget)
        self.mapFilePath = os.path.join('res', 'mapgreyscale.png')
        self._logger = logging.getLogger('pypipboyapp.map.globalmap')
        self.mapZoomLevel = 1.0
        
    def init(self, app, datamanager):
        super().init(app, datamanager)
        # Init graphics view
        self.mapColor = QtGui.QColor.fromRgb(20,255,23)
        self.mapScene = QtWidgets.QGraphicsScene()
        self.mapScene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor.fromRgb(0,0,0)))
        self.mapView = self.widget.mapGraphicsView
        self.mapView.viewport().installEventFilter(self)
        self.mapView.setScene(self.mapScene)
        self.mapView.setMouseTracking(True)
        self.mapView.centerOn(0, 0)
        # Add map graphics
        self.mapItem = MapGraphicsItem(self, self.controller.imageFactory, self.mapFilePath, self.mapColor, True)
        self.signalSetZoomLevel.connect(self.mapItem.setZoomLevel)
        self.signalSetColor.connect(self.mapItem.setColor)
        # Add player marker
        self.playerMarker = PlayerMarker(self,self.controller.imageFactory, self.mapColor)
        self._connectMarker(self.playerMarker)
        self.playerMarker.signalPlayerPositionUpdate.connect(self._slotPlayerMarkerPositionUpdated)
        # Add custom marker
        self.customMarker = CustomMarker(self,self.controller.imageFactory, self.mapColor)
        self._connectMarker(self.customMarker)
        # Add powerarmor marker
        self.powerArmorMarker = PowerArmorMarker(self,self.controller.imageFactory, self.mapColor)
        self._connectMarker(self.powerArmorMarker)
        # Init zoom slider
        self.widget.mapZoomSlider.setMinimum(-100)
        self.widget.mapZoomSlider.setMaximum(100)
        self.widget.mapZoomSlider.setValue(0)
        self.widget.mapZoomSlider.setSingleStep(5)
        self.widget.mapZoomSlider.valueChanged.connect(self._slotZoomSliderTriggered)
        # Init zoom Spinbox
        self.widget.mapZoomSpinbox.setMinimum(self.MAPZOOM_SCALE_MIN*100.0)
        self.widget.mapZoomSpinbox.setMaximum(self.MAPZOOM_SCALE_MAX*100.0)
        self.widget.mapZoomSpinbox.setValue(100.0)
        self.widget.mapZoomSpinbox.setSingleStep(10.0)
        self.widget.mapZoomSpinbox.valueChanged.connect(self._slotZoomSpinTriggered)
        # Init color controls
        self.widget.mapColorButton.clicked.connect(self._slotMapColorSelectionTriggered)
        self.widget.mapColorAutoToggle.stateChanged.connect(self._slotMapColorAutoModeTriggered)
        # Init stickyLabels Checkbox
        self.stickyLabelsEnabled = False
        self.widget.stickyLabelsCheckbox.setChecked(False)
        self.widget.stickyLabelsCheckbox.stateChanged.connect(self._slotStickyLabelsTriggered)
        # Init PowerMarker Enable Checkbox
        self.widget.powerMarkerEnableCheckbox.setChecked(True)
        self.widget.powerMarkerEnableCheckbox.stateChanged.connect(self._slotPowerMarkerEnableTriggered)
        # Init Location Enable Checkbox
        self.locationFilterEnableFlag = True
        self.widget.locationMarkerEnableCheckbox.setChecked(True)
        self.widget.locationMarkerEnableCheckbox.stateChanged.connect(self._slotLocationEnableTriggered)
        # Init Location Visibility Cheat Checkbox
        self.locationVisibilityCheatFlag = False
        self.widget.locationVisibilityCheatCheckbox.setChecked(False)
        self.widget.locationVisibilityCheatCheckbox.stateChanged.connect(self._slotLocationVisibilityCheatTriggered)
        # Init CenterOnPlayer checkbox
        self.centerOnPlayerEnabled = False
        self.widget.centerPlayerCheckbox.setChecked(False)
        self.widget.centerPlayerCheckbox.stateChanged.connect(self._slotCenterOnPlayerCheckToggled)
        # Init SaveTo Button
        self.widget.saveToButton.clicked.connect(self._slotSaveToTriggered)
        # Init PyPipboy stuff
        from .controller import MapCoordinates
        self.mapCoords = MapCoordinates()
        self.datamanager = datamanager
        self.pipMapObject = None
        self.pipMapWorldObject = None
        self.pipColor = None
        self.pipWorldQuests = None
        self.pipMapQuestsItems = dict()
        self.pipWorldLocations = None
        self.pipMapLocationItems = dict()
        self._signalPipWorldQuestsUpdated.connect(self._slotPipWorldQuestsUpdated)
        self._signalPipWorldLocationsUpdated.connect(self._slotPipWorldLocationsUpdated)
        self.datamanager.registerRootObjectListener(self._onRootObjectEvent)

    def _connectMarker(self, marker):
        self.signalSetZoomLevel.connect(marker.setZoomLevel)
        self.signalSetColor.connect(marker.setColor)
        self.signalSetStickyLabel.connect(marker.setStickyLabel)
        marker.signalMarkerDestroyed.connect(self._disconnectMarker)
        if marker.markerType == 4:
            self.signalLocationFilterSetVisible.connect(marker.filterSetVisible)
            self.signalLocationFilterVisibilityCheat.connect(marker.filterVisibilityCheat)
        
    @QtCore.pyqtSlot(QtCore.QObject)
    def _disconnectMarker(self, marker):
        marker.signalMarkerDestroyed.disconnect(self._disconnectMarker)
        self.signalSetZoomLevel.disconnect(marker.setZoomLevel)
        self.signalSetStickyLabel.disconnect(marker.setStickyLabel)
        self.signalSetColor.disconnect(marker.setColor)
        if marker.markerType == 4:
            self.signalLocationFilterSetVisible.disconnect(marker.filterSetVisible)
            self.signalLocationFilterVisibilityCheat.disconnect(marker.filterVisibilityCheat)
    
    def _onRootObjectEvent(self, rootObject):
        self.pipMapObject = rootObject.child('Map')
        if self.pipMapObject:
            self.pipMapObject.registerValueUpdatedListener(self._onPipMapReset)
            self._onPipMapReset(None, None, None)
                
    def _onPipMapReset(self, caller, value, pathObjs):
        self.pipMapWorldObject = self.pipMapObject.child('World')
        if self.pipMapWorldObject:
            extents = self.pipMapWorldObject.child('Extents')
            if extents:
                self.mapCoords.init( 
                        extents.child('NWX').value(), extents.child('NWY').value(), 
                        extents.child('NEX').value(),  extents.child('NEY').value(), 
                        extents.child('SWX').value(), extents.child('SWY').value(), 
                        self.mapItem.MAP_NWX, self.mapItem.MAP_NWY, 
                        self.mapItem.MAP_NEX, self.mapItem.MAP_NEY, 
                        self.mapItem.MAP_SWX, self.mapItem.MAP_SWY )
            else:
                self._logger.warn('No "Extents" record found. Map coordinates may be off')
            if self.widget.mapColorAutoToggle.isChecked():
                self._slotMapColorAutoModeTriggered(True)
            pipWorldPlayer = self.pipMapWorldObject.child('Player')
            if pipWorldPlayer:
                self.playerMarker.setPipValue(pipWorldPlayer, self.datamanager, self.mapCoords)
            pipWorldCustom = self.pipMapWorldObject.child('Custom')
            if pipWorldCustom:
                self.customMarker.setPipValue(pipWorldCustom, self.datamanager, self.mapCoords)
            pipWorldPower = self.pipMapWorldObject.child('PowerArmor')
            if pipWorldPower:
                self.powerArmorMarker.setPipValue(pipWorldPower, self.datamanager, self.mapCoords)
            self.pipWorldQuests = self.pipMapWorldObject.child('Quests')
            if self.pipWorldQuests:
                self.pipWorldQuests.registerValueUpdatedListener(self._onPipWorldQuestsUpdated, 0)
                self._signalPipWorldQuestsUpdated.emit()
            self.pipWorldLocations = self.pipMapWorldObject.child('Locations')
            if self.pipWorldLocations:
                self.pipWorldLocations.registerValueUpdatedListener(self._onPipWorldLocationsUpdated, 0)
                self._signalPipWorldLocationsUpdated.emit()
                    
    def _onPipWorldQuestsUpdated(self, caller, value, pathObjs):
        self._signalPipWorldQuestsUpdated.emit()

    @QtCore.pyqtSlot() 
    def _slotPipWorldQuestsUpdated(self):
        newDict = dict()
        for q in self.pipWorldQuests.value():
            if q.pipId in self.pipMapQuestsItems:
                marker = self.pipMapQuestsItems[q.pipId]
                newDict[q.pipId] = marker
                del self.pipMapQuestsItems[q.pipId]
            else:
                marker = QuestMarker(self,self.controller.imageFactory, self.mapColor)
                self._connectMarker(marker)
                marker.setStickyLabel(self.stickyLabelsEnabled, False)
                marker.setZoomLevel(self.mapZoomLevel, 0.0, 0.0, False)
                marker.setPipValue(q, self.datamanager, self.mapCoords)
                newDict[q.pipId] = marker
        for i in self.pipMapQuestsItems:
            self.pipMapQuestsItems[i].destroy()
        self.pipMapQuestsItems = newDict
                    
                    
    def _onPipWorldLocationsUpdated(self, caller, value, pathObjs):
        self._signalPipWorldLocationsUpdated.emit()

    @QtCore.pyqtSlot() 
    def _slotPipWorldLocationsUpdated(self):
        newDict = dict()
        for l in self.pipWorldLocations.value():
            if l.pipId in self.pipMapLocationItems:
                marker = self.pipMapLocationItems[l.pipId]
                newDict[l.pipId] = marker
                del self.pipMapLocationItems[l.pipId]
            else:
                marker = LocationMarker(self,self.controller.imageFactory, self.mapColor)
                self._connectMarker(marker)
                marker.setStickyLabel(self.stickyLabelsEnabled, False)
                marker.setZoomLevel(self.mapZoomLevel, 0.0, 0.0, False)
                marker.filterSetVisible(self.locationFilterEnableFlag, False)
                marker.filterVisibilityCheat(self.locationVisibilityCheatFlag, False)
                marker.setPipValue(l, self.datamanager, self.mapCoords)
                newDict[l.pipId] = marker
        for i in self.pipMapLocationItems:
            self.pipMapLocationItems[i].destroy()
        self.pipMapLocationItems = newDict
        

    @QtCore.pyqtSlot()        
    def _slotMapColorSelectionTriggered(self):
        color = QtWidgets.QColorDialog.getColor(self.mapColor, self)
        if color.isValid:
            self.signalSetColor.emit(color)


    @QtCore.pyqtSlot(int)        
    def _slotZoomSliderTriggered(self, zoom):
        if zoom == 0:
            mod = 0.0
        elif zoom > 0:
            mod = (self.MAPZOOM_SCALE_MAX - 1) * float(zoom)/100.0
        else:
            mod = (1 -self.MAPZOOM_SCALE_MIN) * float(zoom)/100.0
        viewport = self.mapView.mapToScene(self.mapView.rect())
        centerpos = (viewport.at(2) + viewport.at(0))/2 # (SE + NW)/2
        mcenterpos = centerpos / self.mapZoomLevel # account for previous zoom 
        self.mapZoomLevel = 1+mod
        self.widget.mapZoomSpinbox.blockSignals(True)
        self.widget.mapZoomSpinbox.setValue(self.mapZoomLevel*100.0)
        self.widget.mapZoomSpinbox.blockSignals(False)
        self.signalSetZoomLevel.emit(self.mapZoomLevel, mcenterpos.x(), mcenterpos.y())
        
        
    @QtCore.pyqtSlot(float)        
    def _slotZoomSpinTriggered(self, zoom):
        viewport = self.mapView.mapToScene(self.mapView.rect())
        centerpos = (viewport.at(2) + viewport.at(0))/2 # (SE + NW)/2
        mcenterpos = centerpos / self.mapZoomLevel # account for previous zoom 
        self.mapZoomLevel = zoom/100.0
        if self.mapZoomLevel == 1.0:
            sliderValue = 0
        elif self.mapZoomLevel > 1.0:
            sliderValue = (self.mapZoomLevel/self.MAPZOOM_SCALE_MAX)*100.0
        else:
            sliderValue = -(self.MAPZOOM_SCALE_MIN/self.mapZoomLevel)*100.0
        self.widget.mapZoomSlider.blockSignals(True)
        self.widget.mapZoomSlider.setValue(sliderValue)
        self.widget.mapZoomSlider.blockSignals(False)
        self.signalSetZoomLevel.emit(self.mapZoomLevel, mcenterpos.x(), mcenterpos.y())
        
        
    @QtCore.pyqtSlot(bool)        
    def _slotStickyLabelsTriggered(self, value):
        self.stickyLabelsEnabled = value
        self.signalSetStickyLabel.emit(value)
        
    @QtCore.pyqtSlot(bool)        
    def _slotPowerMarkerEnableTriggered(self, value):
        self.powerArmorMarker.filterSetVisible(value)
        
    @QtCore.pyqtSlot(bool)        
    def _slotLocationEnableTriggered(self, value):
        self.locationFilterEnableFlag = value
        self.signalLocationFilterSetVisible.emit(value)
        
    @QtCore.pyqtSlot(bool)        
    def _slotLocationVisibilityCheatTriggered(self, value):
        self.locationVisibilityCheatFlag = value
        self.signalLocationFilterVisibilityCheat.emit(value)
        
    @QtCore.pyqtSlot(bool)        
    def _slotCenterOnPlayerCheckToggled(self, value):
        self.centerOnPlayerEnabled = value
        if value and self.playerMarker.markerItem.isVisible():
            self.mapView.centerOn(self.playerMarker.markerItem.pos())
            
    @QtCore.pyqtSlot(float, float, float)        
    def _slotPlayerMarkerPositionUpdated(self, x, y, r):
        if self.centerOnPlayerEnabled:
            self.mapView.centerOn(self.playerMarker.markerItem.pos())
        
    @QtCore.pyqtSlot(bool)        
    def _slotMapColorAutoModeTriggered(self, value):
        if self.pipMapObject:
            if value:
                self.pipColor = self.pipMapObject.pipParent.child('Status').child('EffectColor')
                self.pipColor.registerValueUpdatedListener(self._onPipColorChanged, 1)
                self._onPipColorChanged(None, None, None)
            elif self.pipColor:
                self.pipColor.unregisterValueUpdatedListener(self._onPipColorChanged)
            
        
    @QtCore.pyqtSlot()
    def _slotSaveToTriggered(self):
        fileName = QtWidgets.QFileDialog.getSaveFileName(self, '', '', 'Images (*.png *.jpg *.gif)')
        if fileName:
            pixmap = self.mapView.grab()
            pixmap.save(fileName[0])
            
    def _onPipColorChanged(self, caller, value, pathObjs):
        if self.pipColor:
            r = self.pipColor.child(0).value() * 255
            g = self.pipColor.child(1).value() * 255
            b = self.pipColor.child(2).value() * 255
            self.mapColor = QtGui.QColor.fromRgb(r,g,b)
            self.signalSetColor.emit(self.mapColor)

    def eventFilter(self, watched, event):
        if watched == self.mapView.viewport():
            if event.type() == QtCore.QEvent.Wheel:
                # Zoom to center
                viewport = self.mapView.mapToScene(self.mapView.rect())
                centerpos = (viewport.at(2) + viewport.at(0))/2 # (SE + NW)/2
                vcenterpos = centerpos / self.mapZoomLevel # account for previous zoom 
                # Sometimes I get strange angle readings (especially after mouse move)
                #zoom = self.mapZoomLevel + event.angleDelta().y()/120 * 0.1
                if event.angleDelta().y() > 0:
                    zoom = self.mapZoomLevel * 1.1
                else:
                    zoom = self.mapZoomLevel * 0.9
                if zoom < self.MAPZOOM_SCALE_MIN:
                    zoom = self.MAPZOOM_SCALE_MIN
                elif zoom > self.MAPZOOM_SCALE_MAX:
                    zoom = self.MAPZOOM_SCALE_MAX
                if self.mapZoomLevel != zoom:
                    self.mapZoomLevel = zoom
                    if self.mapZoomLevel == 1.0:
                        sliderValue = 0
                    elif self.mapZoomLevel > 1.0:
                        sliderValue = (self.mapZoomLevel/self.MAPZOOM_SCALE_MAX)*100.0
                    else:
                        sliderValue = -(self.MAPZOOM_SCALE_MIN/self.mapZoomLevel)*100.0
                    self.widget.mapZoomSlider.blockSignals(True)
                    self.widget.mapZoomSlider.setValue(sliderValue)
                    self.widget.mapZoomSlider.blockSignals(False)
                    self.widget.mapZoomSpinbox.blockSignals(True)
                    self.widget.mapZoomSpinbox.setValue(self.mapZoomLevel*100.0)
                    self.widget.mapZoomSpinbox.blockSignals(False)
                    self.signalSetZoomLevel.emit(self.mapZoomLevel, vcenterpos.x(), vcenterpos.y())
                return True
            elif event.type() == QtCore.QEvent.ContextMenu:
                if self.mapCoords.isValid:
                    menu = QtWidgets.QMenu(self.mapView)
                    markerPos = self.mapView.mapToScene(event.pos())
                    # Check whether we clicked on a marker
                    if self.mapScene.itemAt(markerPos, QtGui.QTransform()) != self.mapItem.mapItem:
                        return False
                    markerPos = markerPos/self.mapZoomLevel # Account for zoom
                    @QtCore.pyqtSlot()
                    def _setCustomMarker():
                        self.datamanager.rpcSetCustomMarker(self.mapCoords.map2pip_x(markerPos.x()), self.mapCoords.map2pip_y(markerPos.y()))
                    action = menu.addAction('Set Custom Marker')
                    action.triggered.connect(_setCustomMarker)
                    menu.exec(event.globalPos())
                return True
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                
                if self.mapCoords.isValid:
                    markerPos = self.mapView.mapToScene(event.pos())
                    # Check whether we clicked on a marker
                    if self.mapScene.itemAt(markerPos, QtGui.QTransform()) != self.mapItem.mapItem:
                        return False
                    markerPos = markerPos/self.mapZoomLevel # Account for zoom
                    self.datamanager.rpcSetCustomMarker(self.mapCoords.map2pip_x(markerPos.x()), self.mapCoords.map2pip_y(markerPos.y()))
                return True
        return False
        