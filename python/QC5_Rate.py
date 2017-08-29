from subprocess import CalledProcessError
from wrappers import runCommand,envCheck
from PlotOptions import parser
import os

(args,opts)=parser.parse_args()

envCheck('GEM_BASE')
dataPath  = os.getenv('GEM_BASE')
cmd = ["python","%s/python/Produce_Config_File.py"%(dataPath)]

for filelist in args.file:
	cmd.append("--file=%s"%(filelist))
	pass

cmd.append("--CanvTitleX=Divider Current #left(#muA#right)")
cmd.append("--CanvTitleY=Rate #left(Hz#right)")
cmd.append("--LatexLines=0.19,0.88, LS2~Detector~Production")
cmd.append("--LatexLines=0.19,0.83, Gas~=~Ar/CO_{2}~#left(70/30#right)")
cmd.append("--LatexLines=0.19,0.78, X-Ray~Target:~Ag")
cmd.append("--LatexLines=0.19,0.73, X-Ray~V_{mon}~=~40~kV")
cmd.append("--LatexLines=0.19,0.68, X-Ray~I_{mon}~~~=~5~#muA")
cmd.append("--LatexLines=0.19,0.63, i#eta~=~4;~i#phi~=~2")
cmd.append("--SelectColumnX=4")
cmd.append("--SelectColumnY=7")
cmd.append("--SelectRowStart=29")
cmd.append("--SelectRowEnd=45")
cmd.append("--CanvRangeX=0,750")
cmd.append("--CanvRangeY=0,1800")
cmd.append("--SetErrY")
cmd.append("--SelectColumnErrY=8")

if len(args.file)==1:
	filetype=filelist[int(filelist.index('.')):]
	filename = filelist
	filename= filename.replace(filetype,"")
	cmd.append("--OutputName=config_Rate_vs_Imon_"+filename)
	pass
else:
	cmd.append("--OutputName=config_QC5_LS2_Rate_vs_Imon_AllDet")
	pass

runCommand(cmd)