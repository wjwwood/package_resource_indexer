cmake_minimum_required(VERSION 2.8.3)
project(pkg2)

find_package(package_resource_indexer REQUIRED)

register_package(${PROJECT_NAME})
