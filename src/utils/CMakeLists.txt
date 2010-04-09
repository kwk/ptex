# Configure the ptxinfo executable
add_executable(ptxinfo ptxinfo.cpp)
prefix_hack(ptxinfo)

# Make Ptex source files available for include in this project
include_directories(${CMAKE_SOURCE_DIR}/ptex)

# This will append a "d" to the binary's filename (e.g. ptxinfo -> ptxinfod)
set_target_properties(ptxinfo PROPERTIES DEBUG_POSTFIX "${debug_suffix}")

# Specify libraries to link against
target_link_libraries(ptxinfo ${libs} ptex)

# Specify the name of the poject in IDEs
set_target_properties(ptxinfo PROPERTIES PROJECT_LABEL "Ptex Utils (PTXINFO)")

# Install configuration for the ptxinfo executable
install(TARGETS ptxinfo	
		RUNTIME DESTINATION bin			    
        LIBRARY DESTINATION lib
		ARCHIVE DESTINATION	lib)
