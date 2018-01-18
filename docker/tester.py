from subprocess import call
import argparse, sys, os, inspect

# recipe from
# https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python/377028#377028
def which(program):
  import os
  def is_exe(fpath):
      return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

  fpath, fname = os.path.split(program)
  if fpath:
    if is_exe(program):
      return program
  else:
    for path in os.environ["PATH"].split(os.pathsep):
      exe_file = os.path.join(path, program)
      if is_exe(exe_file):
        return exe_file
  return None

class dcmheatReconstructors:

  # volume reconstruction routines
  # assume the actual binary performing the reconstruction is in the path
  # input folder is the directory with DICOM files (for now, assume this is
  # single series corresponding to a 3d volume)
  # output is a tuple of the reconstructed volume and metadata files
  @staticmethod
  def plastimatchReconstructor(inputFolder, outputFolder):
    if not which("plastimatch"):
      print("plastimatch not found - skipping")
      return (None,None)
    # plastimatch outputs output volume in any format supported by ITK
    outputVolume = os.path.join(outputFolder,"volume.nrrd")
    stdoutFile = open(os.path.join(outputFolder,"stdout.log"),"w")
    stderrFile = open(os.path.join(outputFolder,"stderr.log"),"w")
    call(["plastimatch","convert","--input",inputFolder,"--output-img",outputVolume], stdout=stdoutFile, stderr=stderrFile)
    return (outputVolume, None)

  @staticmethod
  def dcm2niixReconstructor(inputFolder, outputFolder):
    if not which("dcm2niix"):
      print("dcm2niix not found - skipping")
      return (None,None)
    # dcm2niix takes output directory and prefix for the output files, and it
    #  does output metadata in JSON
    stdoutFile = open(os.path.join(outputFolder,"stdout.log"),"w")
    stderrFile = open(os.path.join(outputFolder,"stderr.log"),"w")
    call(["dcm2niix","-f","volume","-o",outputFolder,inputFolder], stdout=stdoutFile, stderr=stderrFile)
    outputVolume = os.path.join(outputFolder,"volume.nii")
    outputMetadata = os.path.join(outputFolder,"meta.json")
    return (outputVolume,outputMetadata)

  @staticmethod
  def dicom2niftiReconstructor(inputFolder, outputFolder):
    if not which("dicom2nifti"):
      print("dicom2nifti not found - skipping")
      return (None,None)
    # dcm2niix takes output directory and prefix for the output files, and it
    #  does output metadata in JSON
    stdoutFile = open(os.path.join(outputFolder,"stdout.log"),"w")
    stderrFile = open(os.path.join(outputFolder,"stderr.log"),"w")
    call(["dicom2nifti",inputFolder,outputFolder], stdout=stdoutFile, stderr=stderrFile)
    volumeName = os.listdir(outputFolder)
    if len(volumeName):
      volumeName = volumeName[0]
    outputVolume = os.path.join(outputFolder,volumeName)
    return (outputVolume,None)

def runTests(topLevelInputFolder,topLevelOutputFolder):
  print("Will run tests with "+topLevelInputFolder+" "+topLevelOutputFolder)

  # get all reconstruction fiunctions
  reconFunctions = inspect.getmembers(dcmheatReconstructors)
  reconFunctions = [m[0] for m in reconFunctions if m[0].endswith("Reconstructor")]
  print("All reconstruction funtions: "+str(reconFunctions))

  # assume fixed directory structure for test data, and organize output
  for dataset in os.listdir(topLevelInputFolder):
    print("> Dataset: "+dataset)
    if dataset.startswith("."):
      continue
    for reconstructor in reconFunctions:
      print(" >> Reconstructor: "+reconstructor)
      reconstructorCall = getattr(dcmheatReconstructors, reconstructor)
      inputFolder = os.path.join(topLevelInputFolder,dataset,"in")
      outputFolder = os.path.join(topLevelOutputFolder,dataset,reconstructor.split("Reconstructor")[0])
      if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
      (volume,meta) = reconstructorCall(inputFolder,outputFolder)


  return

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="")
  parser.add_argument("-i","--input-data-directory", dest="topLevelInputFolder", metavar="PATH", required=True)
  parser.add_argument("-o","--output-data-directory", dest="topLevelOutputFolder", metavar="PATH", required=True)

  args = parser.parse_args(sys.argv[1:])

  runTests(args.topLevelInputFolder, args.topLevelOutputFolder)
