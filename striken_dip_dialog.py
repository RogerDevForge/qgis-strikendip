# -*- coding: utf-8 -*-
"""
/***************************************************************************
 StrikenDipDialog
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

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'striken_dip_dialog_base.ui'))


class StrikenDipDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(StrikenDipDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        # Connect signals and slots
        self.cmbStructureType.currentTextChanged.connect(self.on_structure_type_changed)

    def on_structure_type_changed(self, structure_type):
        """Adjust symbol size based on structure type"""
        if structure_type == "Bedding":
            self.spbSymbolSize.setValue(2.5)
        elif structure_type == "Foliation":
            self.spbSymbolSize.setValue(2.0)
        elif structure_type == "Joint":
            self.spbSymbolSize.setValue(1.5)
        elif structure_type == "Fault":
            self.spbSymbolSize.setValue(3.0)
        elif structure_type == "Vein":
            self.spbSymbolSize.setValue(2.0)