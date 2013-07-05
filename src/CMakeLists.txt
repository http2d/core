set (SRC_SERVER 
	Socket.cpp Socket.h 
	Connection.cpp Connection.h
)

add_library(
    server
    SHARED
    ${SRC_SERVER}
    ${INCLUDE_FILES} ${LIBEVENT_INCLUDE_DIR}
)

INCLUDE_DIRECTORIES( ${Boost_INCLUDE_DIR} ${CMAKE_BINARY_DIR} )
ADD_EXECUTABLE( h2main main.cpp )
TARGET_LINK_LIBRARIES( h2main server ${Boost_LIBRARIES} )
