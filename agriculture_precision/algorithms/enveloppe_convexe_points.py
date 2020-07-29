## -*- coding: utf-8 -*-

"""
/***************************************************************************
 AgriculturePrecision
                                 A QGIS plugin
 Chaines de traitement
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-07-21
        copyright            : (C) 2020 by ASPEXIT
        email                : cleroux@aspexit.com
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

__author__ = 'ASPEXIT'
__date__ = '2020-07-21'
__copyright__ = '(C) 2020 by ASPEXIT'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsApplication,
                       QgsVectorLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterVectorDestination)



from qgis import processing 


class EnveloppeConvexePoints(QgsProcessingAlgorithm):
    """
    
    """ 

    OUTPUT= 'OUTPUT'
    INPUT = 'INPUT'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('Couche vecteur à traiter'),
                [QgsProcessing.TypeVectorPoint]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.OUTPUT,
                self.tr('Enveloppe')
            )
        )
        
        

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        
        # Regrouper
        alg_params = {
            'FIELD': None,
            'INPUT': parameters[self.INPUT],
            'OUTPUT': 'memory:'
        }
        alg_result = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        couche_groupee = alg_result['OUTPUT']

        # Enveloppe convexe
        alg_params = {
            'INPUT': couche_groupee,
            'OUTPUT': parameters[self.OUTPUT]
        }
        alg_result = processing.run('native:convexhull', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        
        enveloppe_conv = alg_result['OUTPUT']
        
        return{self.OUTPUT : enveloppe_conv} 
   
    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "Réaliser une enveloppe convexe à partir de points"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Action sur Vecteurs')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'action_sur_vecteur'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return EnveloppeConvexePoints()
