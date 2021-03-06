#!/bin/env python2.7

# -*- coding: utf-8 -*-
#
#    """
#    Created on Saturday April 1
#    
#    @author: Brian L. Dorney
#    """

#Imports
import sys, os
import math
import numpy as np
from ROOT import gROOT, Double, TDirectory, TF1, TFile

#Container for storing fit parameters for a given observable
#Here the observable is described by f(x) = exp(P0*x+P1)
#There exists a function for the average, max, and min of the observable
class PARAMS_OBS_FIT:
    def __init__(self, name):
        self.NAME = name

        self.AVG_P0 = 0.0
        self.AVG_P1 = 0.0

        self.MAX_P0 = 0.0
        self.MAX_P1 = 0.0

        self.MIN_P0 = 0.0
        self.MIN_P1 = 0.0

        return

class PARAMS_TFILE_INPUT:
    #Here:
    #   inputFileName -> physical filename of the desired TFile
    #   inputDetName  -> detector's serial number
    #   inputTObjStr  -> string used to identify the detector in stored TObject's found in inputFileName
    def __init__(self, inputFileName, inputDetName, inputTObjStr):
        self.NAME_FILE  = inputFileName
        self.NAME_DET   = inputDetName
        self.NAME_TOBJ  = inputTObjStr

        return

class HVSetPoint:
    def __init__(self, inputGainVal, debug=False):
	self.DEBUG	= debug

        self.GAIN_VAL   = inputGainVal

        self.LIST_INPUT_FILES		= []
        self.LIST_FIT_PARAMS_GAIN	= []
        self.LIST_FIT_PARAMS_PD		= []

        return

    def setGainValue(self, inputGainVal):
        self.GAIN_VAL = inputGainVal

    def addInputFile(self, inputFileName, inputDetName, inputTObjStr):
        paramsInputFile = PARAMS_TFILE_INPUT(inputFileName, inputDetName, inputTObjStr)

        self.LIST_INPUT_FILES.append(paramsInputFile)

        return

    def printFileList(self):
        for iFile in range(0,len(self.LIST_INPUT_FILES)):
            print self.LIST_INPUT_FILES[iFile].NAME_FILE + "\t" + self.LIST_INPUT_FILES[iFile].NAME_DET + "\t" + self.LIST_INPUT_FILES[iFile].NAME_TOBJ

        return

    def loadFitParams(self, inputList, inputObsName="EffGain"):
        #Loop over files
        for iFile in range(0,len(self.LIST_INPUT_FILES)):
	    #Print debugging information
	    if self.DEBUG:
		print "Processing " + str(iFile) + "th file: " +  self.LIST_INPUT_FILES[iFile].NAME_FILE

            #Get the i^th input file
            thisFile = TFile(self.LIST_INPUT_FILES[iFile].NAME_FILE, "READ", "", 1)

            #Load the fits
            fit_Obs_Avg = thisFile.Get("fit_" + self.LIST_INPUT_FILES[iFile].NAME_TOBJ + "_" + inputObsName + "Avg")
            fit_Obs_Max = thisFile.Get("fit_" + self.LIST_INPUT_FILES[iFile].NAME_TOBJ + "_" + inputObsName + "Max")
            fit_Obs_Min = thisFile.Get("fit_" + self.LIST_INPUT_FILES[iFile].NAME_TOBJ + "_" + inputObsName +  "Min")

	    #Print debugging information
	    if self.DEBUG:
		print "fit_" + self.LIST_INPUT_FILES[iFile].NAME_TOBJ + "_" + inputObsName + "Avg"
		print "fit_Obs_Avg.GetName() = " + fit_Obs_Avg.GetName()
		print "fit_" + self.LIST_INPUT_FILES[iFile].NAME_TOBJ + "_" + inputObsName + "Max"
		print "fit_Obs_Max.GetName() = " + fit_Obs_Avg.GetName()
		print "fit_" + self.LIST_INPUT_FILES[iFile].NAME_TOBJ + "_" + inputObsName +  "Min"
		print "fit_Obs_Min.GetName() = " + fit_Obs_Avg.GetName()

            #Get & store the fit parameters - Gain
            params_obs_fit         = PARAMS_OBS_FIT(self.LIST_INPUT_FILES[iFile].NAME_DET)
            params_obs_fit.AVG_P0  = fit_Obs_Avg.GetParameter(0)
            params_obs_fit.AVG_P1  = fit_Obs_Avg.GetParameter(1)
            params_obs_fit.MAX_P0  = fit_Obs_Max.GetParameter(0)
            params_obs_fit.MAX_P1  = fit_Obs_Max.GetParameter(1)
            params_obs_fit.MIN_P0  = fit_Obs_Min.GetParameter(0)
            params_obs_fit.MIN_P1  = fit_Obs_Min.GetParameter(1)

            #append the given list
            inputList.append(params_obs_fit)
                
            #Close the File
            thisFile.Close()

        return

    def printFitParamGain(self):
	print "Det\tAvgP0\tAvgP1\tMaxP0\tMaxP1\tMinP0\tMinP1"
        for i in range(0, len(self.LIST_FIT_PARAMS_GAIN)):
            printedString = self.LIST_FIT_PARAMS_GAIN[i].NAME + "\t"
            printedString = printedString + str(self.LIST_FIT_PARAMS_GAIN[i].AVG_P0) + "\t"
            printedString = printedString + str(self.LIST_FIT_PARAMS_GAIN[i].AVG_P1) + "\t"
            printedString = printedString + str(self.LIST_FIT_PARAMS_GAIN[i].MAX_P0) + "\t"
            printedString = printedString + str(self.LIST_FIT_PARAMS_GAIN[i].MAX_P1) + "\t"
            printedString = printedString + str(self.LIST_FIT_PARAMS_GAIN[i].MIN_P0) + "\t"
            printedString = printedString + str(self.LIST_FIT_PARAMS_GAIN[i].MIN_P1)
            
            print printedString

        return

    def calculateHVPt(self, printGain=1, printPD=0):
        #Print a table for Gain
        if printGain:
            print "Det\tHVSetPt\tMinGain\tAvgGain\tMaxGain"
            for i in range(0,len(self.LIST_FIT_PARAMS_GAIN)):
                hvVal = ( 1. / self.LIST_FIT_PARAMS_GAIN[i].AVG_P0 ) * ( math.log(self.GAIN_VAL) - self.LIST_FIT_PARAMS_GAIN[i].AVG_P1 )
    
                gain_Max = math.exp( self.LIST_FIT_PARAMS_GAIN[i].MAX_P0 * hvVal + self.LIST_FIT_PARAMS_GAIN[i].MAX_P1)
                gain_Min = math.exp( self.LIST_FIT_PARAMS_GAIN[i].MIN_P0 * hvVal + self.LIST_FIT_PARAMS_GAIN[i].MIN_P1)
                    
                print self.LIST_FIT_PARAMS_GAIN[i].NAME + "\t" + str(hvVal) + "\t" + str(gain_Min) + "\t" + str(self.GAIN_VAL) + "\t" + str(gain_Max)
                
        #Print a table for P_{D}
        if printPD:
            print "placeholder for now, does nothing"

        return

if __name__ == "__main__":
    from optparse import OptionParser
    
    parser = OptionParser()
    
    #Options - debugging
    parser.add_option("-d","--debug", type="int", dest="debug",
                      help="Print debugging information", metavar="debug")
    parser.add_option("-g","--gain", type="float", dest="gainval",
                      help="Gain value to determine HV Settings at", metavar="gainval")
    parser.add_option("--fileGainMapList", type="string", dest="fileGainMapList",
                      help="Tab delimited file of root file, detector serial number, and Detector_Name from run config file", metavar="fileGainMapList") 
    #Get input options
    (options, args) = parser.parse_args()
    
    #Define the HVSetPoint objcet
    hvSettings = HVSetPoint(options.gainval, options.debug)

    #Add list of files
    import os
    try:
        fileGainMapList = open(options.fileGainMapList, 'r') #tab '\t' delimited file, first line column headings, subsequent lines data: PFN of ROOT File\tDet SN\tDetector_Name
    except Exception as e:
        print '%s does not seem to exist'%(options.fileGainMapList)
        print e
        exit(os.EX_NOINPUT)
        pass
    
    # Loop Over inputs
    for i,line in enumerate(fileGainMapList):
        if line[0] == "#" or not i > 0:
            continue

        # Split the line
        line = line.strip('\n')
        detGainList = line.rsplit('\t') #Physical Filename of ROOT File, Det S/N, Detector_Name

        if len(detGainList) != 3:
            print "Input format incorrect"
            print "I was expecting a tab-delimited file with each line having 3 entries"
            print "But I received:"
            print "\t%s"%(line)
            print "Exiting"
            exit(os.EX_USAGE)

        hvSettings.addInputFile(detGainList[0],detGainList[1],detGainList[2])

    #Print the file list if requested
    if options.debug:
	#Printing input files
        hvSettings.printFileList()

    #Get the fit parameters - gain
    hvSettings.loadFitParams(hvSettings.LIST_FIT_PARAMS_GAIN)

    #Print the fit parameters if requested
    if options.debug:
        hvSettings.printFitParamGain()

    #Calculate HV SetPoint
    hvSettings.calculateHVPt()
