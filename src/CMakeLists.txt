if(${CMAKE_SOURCE_DIR} STREQUAL ${CMAKE_BINARY_DIR})
	message(FATAL_ERROR "CMake generation for Ptex is not allowed within the source directory!
Remove the CMakeCache.txt file and try again from another directory, e.g.:

	rm CMakeCache.txt
	cd ..
	mkdir ptex-build
	cd ptex-build
	cmake ../src
")
endif()

# Specify the projects name
project(ptex)

# Configure CMake
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
if(COMMAND cmake_policy)
      cmake_policy(SET CMP0003 NEW)
endif(COMMAND cmake_policy)

# Put libraries and binaries in the same directory
set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)
set(RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/bin)
set(RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/bin)

# Uninstall target
# http://www.cmake.org/Wiki/CMake_FAQ#Can_I_do_.22make_uninstall.22_with_CMake.3F
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/cmake_uninstall.cmake.in"
               "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake"
               IMMEDIATE @ONLY)
add_custom_target(UNINSTALL "${CMAKE_COMMAND}" -P "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake")

# Whether or not to build static libraries and executables
option(PTEX_STATIC "Build static libraries and executables?" OFF)
if(PTEX_STATIC)
    message(STATUS "PTEX_STATIC option enabled")
    add_definitions(-DPTEX_STATIC)
	
    # We need to change the code generation (runtime library) for Visual Studio here.
    # This configuration works for VS 9 SP1 32 Bit.
    #
    # Info on the shortcuts:
    # /MT stands for Multi-threaded
    # /MD stands for Multi-threaded DLL (not used here)  
    if (MSVC)
       SET(CMAKE_CXX_FLAGS "/nologo /W3 /GX /Gy /YX")
       SET(CMAKE_CXX_FLAGS_DEBUG "/MTd /Z7 /Od")
       SET(CMAKE_CXX_FLAGS_RELEASE "/MT /O2")
       SET(CMAKE_CXX_FLAGS_MINSIZEREL "/MT /O2")
       SET(CMAKE_CXX_FLAGS_RELWITHDEBINFO "/MTd /Z7 /Od")    
    endif()	
else()
    # I believe, this was somehow missing in the original Ptex files.
    # It is only needed for MSVC builds but will be defined for all
    # configurations.
    add_definitions(-DPTEX_EXPORTS)
endif()

# Whether or not to append  a "d" character to debug targets.
set(debug_suffix "")
option(USE_DEBUG_SUFFIX "Append a 'd'-character to debug targets? This does NOT enable debug build!" OFF)
if(USE_DEBUG_SUFFIX)
	message(STATUS "USE_DEBUG_SUFFIX option enabled")
	if(${CMAKE_BUILD_TYPE} MATCHES "Debug")
	    set(debug_suffix "d")
	endif()
endif()

# Add libraries to this variable
set(libs)

# Find zlib package
find_package(ZLIB REQUIRED)
if (ZLIB_FOUND)
    include_directories(${ZLIB_INCLUDE_DIRS})
    SET(libs ${libs} ${ZLIB_LIBRARIES})
endif()

# Compiler specific options
if(UNIX)
	# All unix-like OS's, including Apple OS X (and Cygwin)
	add_definitions(-Wall -pedantic -W -std=c++98 -fPIC)
	
	if (CMAKE_BUILD_TYPE MATCHES "Release")
		add_definitions(-O2 -DNDEBUG)
	else()
		add_definitions(-g -DDEBUG)
	endif()
	
	find_package(Threads REQUIRED)
	if (NOT CMAKE_USE_PTHREADS_INIT)
	    message(FATAL_ERROR "Pthreads must be used as threading library!")
	endif()
	set(libs ${libs} -lm ${CMAKE_THREAD_LIBS_INIT}) 
endif()
if(WIN32) 
	# All windows versions (including Cygwin)	
endif()
if(MINGW) 
	# Mingw compiler on windows
endif()
if(MSVC)
	# Microsoft compiler on windows
	if (CMAKE_BUILD_TYPE MATCHES "Release")
		add_definitions(/DNDEBUG)
	else()
		add_definitions(/DDEBUG)
	endif()	
endif()

# Prefix-hack to remove "Release" and "Debug" directories from targets.
# This must be applied to every library or executable when building with Visual Studio.
function(prefix_hack target)
    if (MSVC)
        set_target_properties(${target} PROPERTIES PREFIX "../")
    endif()
endfunction()

# TODO: (kwk) Extract version using git here.
# TODO: (kwk) Add Ptex version define (PTEX_VER).
#PTEX_SHA = $(shell git rev-list --max-count=1 HEAD)
#PTEX_VER = $(shell git describe $(PTEX_SHA)) ($(PTEX_SHA))
#
#ptxinfo: ptxinfo.cpp $(PTEX)
#	$(CXX) $(CXXFLAGS) -DPTEX_VER='"$(PTEX_VER)"' $^ -o $@ $(LIBS)
set(ptex_major "2")
set(ptex_minor "0")
set(ptex_patch "0")

# Include subprojects
add_subdirectory(ptex)
add_subdirectory(utils)
add_subdirectory(tests)
add_subdirectory(doc)
add_subdirectory(package)