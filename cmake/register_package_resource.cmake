include(CMakeParseArguments)

#
# Register with the resource index that this package provides this resource type
#
# :param package_name: the Python package name
# :type package_name: string
# :param resource_name: name of the resource type
# :type resource_name: string
# :param CONTENT: content of the marker file installed as a result of
#   registering (optional, defaults to an empty file)
# :type CONTENT: string
# :param CONTENT_FILE: location of a .in style file to be passed to
#   configure_file() when generating the marker file as a result of registering
#   and configure_file() is called with @ONLY
#   (optional, conflicts with CONTENT)
# :type CONTENT_FILE: string
#
function(register_package_resource package_name resource_name)
  cmake_parse_arguments(ARG "" "CONTENT;CONTENT_FILE" "" ${ARGN})
  if(ARG_UNPARSED_ARGUMENTS)
    message(FATAL_ERROR "register_package_resource() called with unused arguments: ${ARG_UNPARSED_ARGUMENTS}")
  endif()

  if(ARG_CONTENT AND ARG_CONTENT_FILE)
    message(FATAL_ERROR "register_package_resource() called with both CONTENT and CONTENT_FILE, only one is allowed")
  endif()

  if("${package_name}" STREQUAL "")
    message(FATAL_ERROR "register_package_resource() called with empty string for the 'package_name'")
  endif()

  if("${resource_name}" STREQUAL "")
    message(FATAL_ERROR "register_package_resource() called with empty string for the 'resource_name'")
  endif()

  set(_resource_dir_path "share/resource_index/${resource_name}")
  set(_marker_file_path "${_resource_dir_path}/${package_name}")

  set(_marker_file_build_space_path "${CMAKE_CURRENT_BINARY_DIR}/${_marker_file_path}")

  if(ARG_CONTENT_FILE)
    # Use configure_file() to create the marker file
    if(NOT EXISTS "${ARG_CONTENT_FILE}")
      message(FATAL_ERROR "register_package_resource() given CONTENT_FILE which does not exist: ${ARG_CONTENT_FILE}")
    endif()

    configure_file("${ARG_CONTENT_FILE}" "${_marker_file_build_space_path}" @ONLY)
  else()
    # Use the CONTENT arg to create the marker file
    file(WRITE "${_marker_file_build_space_path}" "${ARG_CONTENT}")
  endif()

  # Install the file
  install(FILES "${_marker_file_build_space_path}" DESTINATION "${_resource_dir_path}")
endfunction()
