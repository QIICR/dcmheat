
exampleCommandLines = '''
docker run --rm -it -p 8080:8080 -v $(pwd)/scripts:/scripts -v $(pwd)/input:/input -v $(pwd)/output:/output:rw -e SLICER_ARGUMENTS="--python-code execfile('/scripts/SlicerConvert.py')" stevepieper/slicer

docker run --rm -it -p 8080:8080 -v $(pwd)/scripts:/scripts -v $(pwd)/input:/input -v $(pwd)/output:/output:rw -e SLICER_ARGUMENTS="--dcmtk --python-code execfile('/scripts/SlicerConvert.py')" stevepieper/slicer
'''

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
args = parser.parse_args()
if args.dcmtk and args.gdcm:
    raise ValueError("Cannot specify both gdcm and dcmtk")
if args.dcmtk:
    setDICOMReaderApproach('DCMTK')
if args.gdcm:
    setDICOMReaderApproach('GDCM')


indexer = ctk.ctkDICOMIndexer()
indexer.addDirectory(slicer.dicomDatabase, '/input')
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

os.system('chmod a+w /output')

for node in slicer.util.getNodesByClass('vtkMRMLScalarVolumeNode'):
    path = os.path.join('/output', node.GetName()+'.nrrd')
    print('Saving to ', path)
    slicer.util.saveNode(node, path)

# request a shutdown of the container
if not args.no_quit:
    os.system('sudo kill -2 1')
