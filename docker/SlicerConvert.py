import os
import sys

def setDICOMReaderApproach(approach):
    import DICOMScalarVolumePlugin
    approaches = DICOMScalarVolumePlugin.DICOMScalarVolumePluginClass.readerApproaches()
    if approach not in approaches:
        raise ValueError("Unknown dicom approach: %s\nValid options are: %s" % (approach, approaches))
    approachIndex = approaches.index(approach)
    settings = qt.QSettings()
    settings.setValue('DICOM/ScalarVolume/ReaderApproach', approachIndex)


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--dcmtk", help="use dcmtk to parse dicom (exclusive with --gdcm)", action="store_true")
parser.add_argument("--gdcm", help="use dcmtk to parse dicom (exclusive with --dcmtk)", action="store_true")
parser.add_argument("--no-quit", help="For debugging, don't exit Slicer after converting", action="store_true")
parser.add_argument("--input", help="Input DICOM directory")
parser.add_argument("--output", help="Output directory")

args = parser.parse_args()
if args.dcmtk and args.gdcm:
    raise ValueError("Cannot specify both gdcm and dcmtk")
if args.dcmtk:
    setDICOMReaderApproach('DCMTK')
if args.gdcm:
    setDICOMReaderApproach('GDCM')

from DICOMLib import DICOMUtils

indexer = ctk.ctkDICOMIndexer()
dbDir = "/tmp/SlicerDB"
print("Temporary directory: "+dbDir)
with DICOMUtils.TemporaryDICOMDatabase(dbDir) as db:
  indexer.addDirectory(db, args.input)
  indexer.waitForImportFinished()

slicer.util.selectModule('DICOM')

popup = slicer.modules.DICOMWidget.detailsPopup
popup.open()

fileLists = []
for patient in slicer.dicomDatabase.patients():
    print(patient)
    for study in slicer.dicomDatabase.studiesForPatient(patient):
        print(study)
        for series in slicer.dicomDatabase.seriesForStudy(study):
            print(series)
            fileLists.append(slicer.dicomDatabase.filesForSeries(series))
print(fileLists)
popup.fileLists = fileLists

popup.examineForLoading()
popup.organizeLoadables()
popup.loadCheckedLoadables()

nodes = slicer.util.getNodesByClass('vtkMRMLScalarVolumeNode')

if len(nodes)>1:
    print("Input dataset resulted in more than one scalar node! Aborting.")
elif len(nodes)==0:
    print("No scalar volumes parsed from the input DICOM dataset! Aborting.")
else:
    path = os.path.join(args.output, 'volume.nrrd')
    print('Saving to ', path)
    slicer.util.saveNode(nodes[0], path)

import shutil
shutil.rmtree(dbDir)

slicer.app.quit()
