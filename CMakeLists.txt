## cmake -G"Eclipse CDT4 - Unix Makefiles" -D CMAKE_BUILD_TYPE=Debug -D_ECLIPSE_VERSION=4.2 -DCMAKE_CXX_COMPILER=g++-mp-4.8 ../h2

# Project
set(PROJECT_NAME_STR h2)
project(${PROJECT_NAME_STR} C CXX)

# CMake version check
cmake_minimum_required(VERSION 2.8)

# C++ version check
include("cmake/set_cxx_norm.cmake")
include("cmake/FindLibEvent.cmake")
set_cxx_norm(CXX_NORM_CXX11)

# Testing
enable_testing()

# Libraries
FIND_PACKAGE( Boost 1.40 COMPONENTS program_options REQUIRED )
FIND_PACKAGE( ZLIB REQUIRED )

# Include directories
add_subdirectory(test)
add_subdirectory(src)

# Distribution
include (CPack)
