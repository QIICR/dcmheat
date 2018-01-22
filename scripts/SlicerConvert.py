
exampleCommandLine = '''
docker run --rm -it -p 8080:8080 -v $(pwd)/scripts:/scripts -v $(pwd)/input:/input -v $(pwd)/output:/output:rw -e SLICER_ARGUMENTS="--python-code execfile('/scripts/SlicerConvert.py')" stevepieper/slicer
'''

import os

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
os.system('sudo kill -2 1')


