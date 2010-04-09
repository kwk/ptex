# Add the ptex source directory to the include path
include_directories(${CMAKE_SOURCE_DIR})

# Pixar's Renderman options
option(PRMAN_15_COMPATIBLE_PTEX "PRMAN_15_COMPATIBLE_PTEX" OFF)
if(PRMAN_15_COMPATIBLE_PTEX)
    message(STATUS "PRMAN_15_COMPATIBLE_PTEX option enabled")	
    add_definitions(-DPTEX_NO_LARGE_METADATA_BLOCKS)
endif()

# Configure the Ptex library
set(srcs
    PtexCache.cpp 
    PtexCache.h 
    PtexDict.h
    PtexFilters.cpp 
    PtexHalf.cpp 
    PtexHalf.h  
    PtexHashMap.h
    PtexInt.h
    PtexIO.h 
    PtexMutex.h
    PtexPlatform.h 
    PtexReader.cpp 
    PtexReader.h
    PtexSeparableFilter.cpp 
    PtexSeparableFilter.h 
    PtexSeparableKernel.cpp 
    PtexSeparableKernel.h
    PtexTriangleFilter.cpp 
    PtexTriangleFilter.h
    PtexTriangleKernel.cpp 
    PtexTriangleKernel.h
    Ptexture.h
    PtexUtils.cpp 
    PtexUtils.h
    PtexWriter.cpp 
    PtexWriter.h)

if(PTEX_STATIC)
	add_library(ptex STATIC ${srcs})
else()
	add_library(ptex SHARED ${srcs})
endif()

prefix_hack(ptex)

# This will append a "d" to the lib's filename (e.g. libPtex.so -> libPtexd.so)
set_target_properties(ptex PROPERTIES DEBUG_POSTFIX "${debug_suffix}")

# Specify libraries to link against
target_link_libraries(ptex ${libs})

# Specify the name of the poject in IDEs
set_target_properties(ptex PROPERTIES PROJECT_LABEL "Ptex Library")

# Install configuration for header files
install(FILES
			Ptexture.h
			PtexHalf.h
			PtexInt.h
			PtexUtils.h 
		DESTINATION include)
			
# Install configuration for the library itself
install(TARGETS ptex				
		RUNTIME DESTINATION bin			    
        LIBRARY DESTINATION lib
		ARCHIVE DESTINATION	lib)
