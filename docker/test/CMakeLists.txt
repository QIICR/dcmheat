project(dcmrec)

include("support.cmake")

enable_testing()

#set(DATA_ROOT "/usr/data")
set(DATA_ROOT "/Users/fedorov/github/dcmheat/docker/data")
file(GLOB data_files "${DATA_ROOT}/*")

message("Glob result: ${data_files}")

foreach(converter_name "slicer" "dcm2niix")
  foreach(data_file ${data_files})
    get_filename_component(file_name ${data_file} NAME)
    message("Filename: ${file_name} ${converter_name}")
    dcm2niix("${data_file}/in" "${data_file}/dcm2niix")
  endforeach()
endforeach()

add_test(echo echo "Test")
