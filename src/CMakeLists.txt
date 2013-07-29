INCLUDE_DIRECTORIES( ${Boost_INCLUDE_DIR} ${CMAKE_BINARY_DIR} )

set (SRC_SERVER 
	Server.cpp Server.h
	Socket.cpp Socket.h 
	Connection.cpp Connection.h
)

add_library(
    server
    SHARED
    ${SRC_SERVER}
    ${INCLUDE_FILES} ${LIBEVENT_INCLUDE_DIR}
)
target_link_libraries (
	server
	${LIBEVENT_LIB} ${Boost_LIBRARIES}
)

ADD_EXECUTABLE( h2main main.cpp )
TARGET_LINK_LIBRARIES( h2main server ${Boost_LIBRARIES} )
