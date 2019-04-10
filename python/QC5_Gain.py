#!/afs/cern.ch/sw/lcg/external/Python/2.7.4/x86_64-slc6-gcc48-opt/bin/python2.7

from subprocess import CalledProcessError
from wrappers import runCommand,envCheck
from PlotOptions import parser
import os

(args,opts)=parser.parse_args()

cmd = ["Produce_Config_File.py"]

for filelist in args.file:
	cmd.append("--file=%s"%(filelist))
	pass

cmd.append("--CanvTitleX=Divider Current #left(#muA#right)")
cmd.append("--CanvTitleY=Effective Gain")
cmd.append("--LatexLines=0.19,0.88, LS2~Detector~Production")
cmd.append("--LatexLines=0.19,0.83, Gas~=~Ar/CO_{2}~#left(70/30#right)")
cmd.append("--LatexLines=0.19,0.78, X-Ray~Target:~Ag")
cmd.append("--LatexLines=0.19,0.73, X-Ray~V_{mon}~=~40~kV")
cmd.append("--LatexLines=0.19,0.68, X-Ray~I_{mon}~~~=~5~#muA")
cmd.append("--LatexLines=0.19,0.63, i#eta~=~4;~i#phi~=~2")
cmd.append("--SelectColumnX=4")
cmd.append("--SelectColumnY=11")
cmd.append("--SelectRowStart=29")
cmd.append("--SelectRowEnd=44")
cmd.append("--CanvRangeX=0,750")
cmd.append("--CanvLogXY=false,true")
cmd.append("--CanvRangeY=10,1000000")
cmd.append("--SetErrY")
cmd.append("--SelectColumnErrY=12")

if len(args.file)==1:
	filetype=filelist[int(filelist.index('.')):]
	filename = filelist
	filename= filename.replace(filetype,"")
	cmd.append("--OutputName=config_Gain_vs_Imon_"+filename)
	pass
else:
	cmd.append("--OutputName=config_QC5_LS2_Gain_vs_Imon_AllDet")
	pass

runCommand(cmd)
