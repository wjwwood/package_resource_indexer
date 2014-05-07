cmake_minimum_required(VERSION 2.8.3)
project(pkg1)

find_package(package_resource_indexer REQUIRED)

register_package(${PROJECT_NAME})
register_package_resource(${PROJECT_NAME} "plugin.rviz.display"
                          CONTENT "../../${PROJECT_NAME}/rviz_plugin.xml")

set(TEST_DEFINE "1")
set(TEST_CURLY_BRACES "should not see this!")
set(TEST_AT_SYMBOL "at symbol works")
register_package_resource(${PROJECT_NAME} "test.content.file"
                          CONTENT_FILE "${CMAKE_CURRENT_SOURCE_DIR}/marker.in")

install(FILES "rviz_plugin.xml" DESTINATION "share/${PROJECT_NAME}")
