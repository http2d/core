## cmake -G"Eclipse CDT4 - Unix Makefiles" -D CMAKE_BUILD_TYPE=Debug -D_ECLIPSE_VERSION=4.2 -DCMAKE_CXX_COMPILER=g++-mp-4.9 ../h2

# Project
set(PROJECT_NAME_STR http2d)
project(${PROJECT_NAME_STR} C CXX)

# CMake version check
cmake_minimum_required(VERSION 2.8)

# Includes
include(CheckTypeSize)
include(CheckIncludeFiles)
include(CheckFunctionExists)
include("cmake/set_cxx_norm.cmake")
include("cmake/FindLibEvent.cmake")

# C++ version check
set_cxx_norm(CXX_NORM_CXX11)

# Headers
macro(HTTP2D_CHECK_INCLUDE INCLUDE VARIABLE)
  CHECK_INCLUDE_FILES (${INCLUDE} ${VARIABLE})
  if(${VARIABLE})
    set(HTTP2D_ALL_INCLUDES "${INCLUDE};${HTTP2D_ALL_INCLUDES}")
  endif()
endmacro()

HTTP2D_CHECK_INCLUDE (sys/time.h HAVE_SYS_TIME_H)
HTTP2D_CHECK_INCLUDE (sys/socket.h HAVE_SYS_SOCKET_H)
HTTP2D_CHECK_INCLUDE (netinet/in.h HAVE_NETINET_IN_H)
HTTP2D_CHECK_INCLUDE (arpa/inet.h HAVE_ARPA_INET_H)
HTTP2D_CHECK_INCLUDE (sys/un.h HAVE_SYS_UN_H)
HTTP2D_CHECK_INCLUDE (sys/socket.h HAVE_SYS_SOCKET_H)

# CHECK_INCLUDE_FILES (sys/time.h HAVE_SYS_TIME_H)
# CHECK_INCLUDE_FILES (sys/socket.h HAVE_SYS_SOCKET_H)
# CHECK_INCLUDE_FILES (netinet/in.h HAVE_NETINET_IN_H)
# CHECK_INCLUDE_FILES (arpa/inet.h HAVE_ARPA_INET_H)
# CHECK_INCLUDE_FILES (sys/un.h HAVE_SYS_UN_H)
# CHECK_INCLUDE_FILES (sys/socket.h HAVE_SYS_SOCKET_H)

# Structs
MESSAGE(STATUS "Detected headers: ${HTTP2D_ALL_INCLUDES}")
SET(CMAKE_EXTRA_INCLUDE_FILES ${HTTP2D_ALL_INCLUDES})
CHECK_TYPE_SIZE ("struct in6_addr" SIZEOF_IN6_ADDR)
CHECK_TYPE_SIZE ("struct sockaddr_un" SIZEOF_SOCKADDR_UN)
CHECK_TYPE_SIZE ("struct sockaddr_in6" SIZEOF_SOCKADDR_IN6)
CHECK_TYPE_SIZE ("long long" SIZEOF_LONG_LONG)

SET(CMAKE_EXTRA_INCLUDE_FILES)

# Testing
enable_testing()

# Libraries
FIND_PACKAGE( Threads REQUIRED )
FIND_PACKAGE( Boost 1.40 COMPONENTS program_options REQUIRED )
FIND_PACKAGE( ZLIB REQUIRED )

# Include directories
add_subdirectory(test)
add_subdirectory(src)

# config.h
execute_process (COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/config.h.in.pre-update.py ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR})
CONFIGURE_FILE (${CMAKE_CURRENT_BINARY_DIR}/config.h.in ${CMAKE_CURRENT_BINARY_DIR}/config.h IMMEDIATE)

# Source distribution
INCLUDE(CPack)

# Final license reminder
MESSAGE ("
+------------------------------------------------------------------+
| License:                                                         |
| This software is subject to the BSD License, available in this   |
| distribution in the file LICENSE. Please, remember that any copy |
| distribution or modification of the software is subject to it.   |
+------------------------------------------------------------------+

Thank you for using ${PROJECT_NAME_STR}.
")