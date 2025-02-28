# -*- coding: utf-8 -*-
"""
/***************************************************************************
 StrikenDip
                                 A QGIS plugin
 A plugin to add strike and dip symbols to geological maps
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2025-02-28
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Your Name
        email                : your.email@example.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QDate, QDateTime
from qgis.PyQt.QtGui import QIcon, QColor
from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.core import (QgsProject, QgsFeature, QgsGeometry, QgsPoint, 
                      QgsVectorLayer, QgsField, QgsSymbol, QgsSvgMarkerSymbolLayer,
                      QgsSingleSymbolRenderer, QgsMarkerSymbol, QgsSimpleMarkerSymbolLayer,
                      QgsLineSymbolLayer, QgsProperty, QgsPalLayerSettings, 
                      QgsVectorLayerSimpleLabeling)
from qgis.gui import QgsMapTool

from PyQt5.QtCore import Qt, QVariant, QPointF
import os.path
import datetime

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .striken_dip_dialog import StrikenDipDialog
# Using direct method for setting angle property
from qgis.core import QgsPropertyCollection

class StrikenDip:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'StrikenDip_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Strike and Dip')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
        
        # Set up the color mapping
        self.color_map = {
            'Black': QColor(0, 0, 0),
            'Red': QColor(255, 0, 0),
            'Blue': QColor(0, 0, 255),
            'Green': QColor(0, 128, 0),
            'Yellow': QColor(255, 255, 0)
        }

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('StrikenDip', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/striken_dip/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Add Strike and Dip'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Strike and Dip'),
                action)
            self.iface.removeToolBarIcon(action)

    def check_or_create_layers(self):
        """Check if required layers exist, if not create them"""
        project = QgsProject.instance()
        strike_dip_layer = None
        
        # Check if Strike and Dip layer exists
        strike_dip_layers = project.mapLayersByName("Strike and Dip Measurements")
        if not strike_dip_layers:
            # Create a new memory layer for Strike and Dip measurements
            strike_dip_layer = QgsVectorLayer("Point?crs=EPSG:4326", "Strike and Dip Measurements", "memory")
            
            # Add fields to the layer
            provider = strike_dip_layer.dataProvider()
            provider.addAttributes([
                QgsField("measurement_id", QVariant.Int),
                QgsField("unit", QVariant.String),
                QgsField("strike", QVariant.Int),
                QgsField("dip", QVariant.Int),
                QgsField("structure_type", QVariant.String),
                QgsField("symbol_size", QVariant.Double),
                QgsField("symbol_color", QVariant.String),
                QgsField("confidence", QVariant.String),
                QgsField("notes", QVariant.String),
                QgsField("measurement_date", QVariant.Date),
                QgsField("created_date", QVariant.DateTime)
            ])
            strike_dip_layer.updateFields()
            
            # Add the layer to the project
            project.addMapLayer(strike_dip_layer)
            return strike_dip_layer
        else:
            return strike_dip_layers[0]

    def get_next_measurement_id(self, layer):
        """Get the next measurement ID by finding the maximum existing ID and adding 1"""
        measurement_id_idx = layer.fields().indexOf("measurement_id")
        max_id = 0
        
        if layer.featureCount() > 0:
            max_id = layer.maximumValue(measurement_id_idx) or 0
            
        return max_id + 1

    def apply_strike_dip_symbology(self, layer):
        """Apply proper symbology to visualize strike and dip symbols"""
        # Create a new marker symbol
        symbol = QgsMarkerSymbol()
        
        # Remove any default symbol layers
        if symbol.symbolLayerCount() > 0:
            symbol.deleteSymbolLayer(0)
        
        # Create the strike line (longer horizontal line)
        strike_line = QgsSimpleMarkerSymbolLayer.create({'name': 'line'})
        strike_line.setColor(QColor(0, 0, 0))
        strike_line.setSize(3.5)  # Length of the strike line
        strike_line.setStrokeWidth(0.4)
        
        # Create the dip line (shorter perpendicular line)
        dip_line = QgsSimpleMarkerSymbolLayer.create({'name': 'line'})
        dip_line.setColor(QColor(0, 0, 0))
        dip_line.setSize(1.5)  # Length of the dip line
        dip_line.setStrokeWidth(0.4)
        # Rotate the dip line 90 degrees relative to the strike line
        dip_line.setAngle(90)
        # Offset the dip line to the "downhill" direction
        dip_line.setOffset(QPointF(0, 0.75))
        
        # Add both lines to the symbol
        symbol.appendSymbolLayer(strike_line)
        symbol.appendSymbolLayer(dip_line)
        
        # Set the rotation of the entire symbol based on the strike value
        # We use property collection for proper data definition
        from qgis.core import QgsProperty, QgsPropertyCollection
        
        # Create a data-defined property for rotation
        rotation_property = QgsProperty.fromExpression("strike")
        
        # Apply rotation to the symbol itself
        prop_collection = QgsPropertyCollection()
        # Property 0 is usually the rotation/angle in most QGIS versions
        # Try different IDs (0, 1, 2, etc.) if this doesn't work
        prop_collection.setProperty(0, rotation_property)
        symbol.setDataDefinedProperties(prop_collection)
        
        # Apply the symbol to the layer
        renderer = QgsSingleSymbolRenderer(symbol)
        layer.setRenderer(renderer)
        
        # Refresh the layer display
        layer.triggerRepaint()

    def run(self):
        """Run method that performs all the real work"""
        
        # Create or check for the required layers
        strike_dip_layer = self.check_or_create_layers()
        
        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = StrikenDipDialog()
            
        # Set current date for measurement date
        self.dlg.dteMeasurement.setDate(QDate.currentDate())
        
        # Get map canvas center coordinates
        mc = self.iface.mapCanvas()
        center = mc.center()
        
        # Set latitude and longitude to map center
        self.dlg.spbLatitude.setValue(center.y())
        self.dlg.spbLongitude.setValue(center.x())
        
        # Show the dialog
        self.dlg.show()
        
        # Run the dialog event loop
        result = self.dlg.exec_()
        
        # See if OK was pressed
        if result:
            # Get values from dialog
            unit = self.dlg.cmbUnit.currentText()
            strike = self.dlg.spbStrike.value()
            dip = self.dlg.spbDip.value()
            structure_type = self.dlg.cmbStructureType.currentText()
            symbol_size = self.dlg.spbSymbolSize.value()
            symbol_color = self.dlg.cmbColor.currentText()
            confidence = self.dlg.cmbConfidence.currentText()
            notes = self.dlg.txtNotes.toPlainText()
            measurement_date = self.dlg.dteMeasurement.date().toPyDate()
            latitude = self.dlg.spbLatitude.value()
            longitude = self.dlg.spbLongitude.value()
            
            # Create a new feature
            feature = QgsFeature(strike_dip_layer.fields())
            
            # Get next measurement ID
            measurement_id = self.get_next_measurement_id(strike_dip_layer)
            
            # Set attributes
            feature.setAttribute("measurement_id", measurement_id)
            feature.setAttribute("unit", unit)
            feature.setAttribute("strike", strike)
            feature.setAttribute("dip", dip)
            feature.setAttribute("structure_type", structure_type)
            feature.setAttribute("symbol_size", symbol_size)
            feature.setAttribute("symbol_color", symbol_color)
            feature.setAttribute("confidence", confidence)
            feature.setAttribute("notes", notes)
            # Make sure measurement_date is a proper date object, not a string
            # If the line above is causing problems, modify it to:
            if isinstance(measurement_date, str) and not measurement_date:
                # If it's an empty string, use current date
                feature.setAttribute("measurement_date", QDate.currentDate().toPyDate())
            else:
                # Otherwise use the date from the form
                feature.setAttribute("measurement_date", measurement_date)
                feature.setAttribute("created_date", QDateTime.currentDateTime())
            
            # Set geometry
            point = QgsGeometry.fromPointXY(center)
            feature.setGeometry(point)
            
            # Add feature to layer
            strike_dip_layer.startEditing()
            strike_dip_layer.addFeature(feature)
            strike_dip_layer.commitChanges()
            
            # Update layer symbology if needed
            self.apply_strike_dip_symbology(strike_dip_layer)
            
            # Show success message
            QMessageBox.information(
                self.dlg, 
                "Success", 
                f"Strike and Dip measurement added:\n\nMeasurement ID: {measurement_id}\nUnit: {unit}\nStrike: {strike}°\nDip: {dip}°\nLocation: ({longitude}, {latitude})"
            )