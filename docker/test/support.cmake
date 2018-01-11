function(dcm2niix inputDir outputFile)
  execute_process(COMMAND "dcm2niix" ${inputDir} "-f" ${outputFile})
endfunction()
