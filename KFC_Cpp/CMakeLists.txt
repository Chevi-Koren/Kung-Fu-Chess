cmake_minimum_required(VERSION 3.16)
project(KungFuChess)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find all source files in src directory
file(GLOB_RECURSE SOURCES "src/*.cpp")
file(GLOB_RECURSE HEADERS "src/*.hpp")

# Create executable
add_executable(${PROJECT_NAME} ${SOURCES} ${HEADERS})

# Set OpenCV paths
set(OPENCV_DIR "${CMAKE_CURRENT_SOURCE_DIR}/OpenCV_451")
set(OPENCV_INCLUDE_DIR "${OPENCV_DIR}/include")
set(OPENCV_LIB_DIR "${OPENCV_DIR}/bin")

# Include directories
target_include_directories(${PROJECT_NAME} PRIVATE ${OPENCV_INCLUDE_DIR})

# Link directories
target_link_directories(${PROJECT_NAME} PRIVATE ${OPENCV_LIB_DIR})

# Link OpenCV libraries - use different libraries for Debug vs Release
target_link_libraries(${PROJECT_NAME} 
    $<$<CONFIG:Debug>:${OPENCV_LIB_DIR}/opencv_world451d.lib>
    $<$<CONFIG:Release>:${OPENCV_LIB_DIR}/opencv_world451.lib>
    $<$<CONFIG:RelWithDebInfo>:${OPENCV_LIB_DIR}/opencv_world451.lib>
    $<$<CONFIG:MinSizeRel>:${OPENCV_LIB_DIR}/opencv_world451.lib>
)

# Copy OpenCV DLLs to output directory
if(WIN32)
    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        $<$<CONFIG:Debug>:${OPENCV_LIB_DIR}/opencv_world451d.dll>
        $<$<CONFIG:Release>:${OPENCV_LIB_DIR}/opencv_world451.dll>
        $<$<CONFIG:RelWithDebInfo>:${OPENCV_LIB_DIR}/opencv_world451.dll>
        $<$<CONFIG:MinSizeRel>:${OPENCV_LIB_DIR}/opencv_world451.dll>
        $<TARGET_FILE_DIR:${PROJECT_NAME}>)
endif()

# Add option to build unit tests ------------------------------------------------
option(KFC_BUILD_TESTS "Build doctest-based unit tests" ON)

# ---------------------------------------------------------------------
# Fetch third-party single-header libraries
# ---------------------------------------------------------------------
include(FetchContent)

# doctest (unit-testing)
FetchContent_Declare(
    doctest
    GIT_REPOSITORY https://github.com/doctest/doctest.git
    GIT_TAG v2.4.11
    SOURCE_SUBDIR .
)
FetchContent_MakeAvailable(doctest)

# nlohmann/json (header-only)
FetchContent_Declare(
    nlohmann_json
    GIT_REPOSITORY https://github.com/nlohmann/json.git
    GIT_TAG v3.11.2
    SOURCE_SUBDIR .
)
FetchContent_MakeAvailable(nlohmann_json)

# Make json include directory available to all targets
set(JSON_INCLUDE_DIR ${nlohmann_json_SOURCE_DIR}/single_include)

# ---------------------------------------------------------------------
# Link libraries + includes for main executable
# ---------------------------------------------------------------------
# Already have target ${PROJECT_NAME}

target_include_directories(${PROJECT_NAME} PRIVATE ${JSON_INCLUDE_DIR})

# ---------------------------------------------------------------------
# Unit tests target adjustments
# ---------------------------------------------------------------------
if(KFC_BUILD_TESTS)
    target_include_directories(kungfu_chess_tests PRIVATE
        ${OPENCV_INCLUDE_DIR}
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        ${JSON_INCLUDE_DIR}
        ${CMAKE_CURRENT_SOURCE_DIR}/extern)

    target_link_libraries(kungfu_chess_tests PRIVATE
        ${PROJECT_NAME}
        doctest::doctest
        nlohmann_json::nlohmann_json)
endif()

# Print found sources for debugging
message(STATUS "Found source files: ${SOURCES}")
message(STATUS "Found header files: ${HEADERS}") 