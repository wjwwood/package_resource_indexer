#
# Register this package with the resource index
#
# :param package_name: the Python package name
# :type package_name: string
#
function(register_package package_name)
  if(ARGN)
    message(FATAL_ERROR "register_package() called with unused arguments: ${ARGN}")
  endif()

  # Use register_package_resource() to register this package
  # in the special 'packages' resource type
  register_package_resource(${package_name} "packages")
endfunction()
