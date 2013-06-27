# Google Test
find_package(GTest REQUIRED)

set(PROJECT_TEST_NAME "${PROJECT_NAME_STR}_test")
include_directories(${GTEST_INCLUDE_DIRS} ${COMMON_INCLUDES} ${CMAKE_CURRENT_SOURCE_DIR}/../src)

add_executable(${PROJECT_TEST_NAME} "test1.cpp")
target_link_libraries(${PROJECT_TEST_NAME} ${GTEST_BOTH_LIBRARIES} ${CMAKE_THREAD_LIBS_INIT})

add_test(${PROJECT_TEST_NAME} ${PROJECT_TEST_NAME})