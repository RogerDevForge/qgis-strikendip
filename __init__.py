# -*- coding: utf-8 -*-
"""
/***************************************************************************
 StrikenDip
                                 A QGIS plugin
 Add a symbol for strike and dip directions, select type of structure and colour.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2025-02-28
        copyright            : (C) 2025 by Roger Roca/TUBAF
        email                : rrocamir@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load StrikenDip class from file StrikenDip.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .striken_dip import StrikenDip
    return StrikenDip(iface)
