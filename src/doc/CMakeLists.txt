find_package(Doxygen)

if(DOXYGEN_FOUND)  
	# Check for the "dot" tool which is part of Graphviz.
	# By setting the "HAVE_DOT" this way, it will automatically
	# replace the value in the Doxyfile file.
    if(DOXYGEN_DOT_EXECUTABLE)
        set(DOXYGEN_HAVE_DOT YES)	
	else()
	    set(DOXYGEN_HAVE_DOT NO)
	    message(STATUS "The 'dot' tool from the Graphviz package could not be found")
	endif()
	
	# To substitute CMake variables in the Doxyfile we configure it
	configure_file(
		${PROJECT_SOURCE_DIR}/doc/Doxyfile
		${PROJECT_BINARY_DIR}/doc/Doxyfile
		ESCAPE_QUOTES
	)
	
	# To substitute CMake variables in the Doxyfile we configure it
	configure_file(
		${PROJECT_SOURCE_DIR}/doc/Doxyfile_API_only
		${PROJECT_BINARY_DIR}/doc/Doxyfile_API_only
		ESCAPE_QUOTES
	)	

	# Create a new doc make target.
	# The DOT_PATH and HAVE_DOT are substituted into the doc/doxyfile.
	add_custom_target(doc ${DOXYGEN} ${PROJECT_BINARY_DIR}/doc/Doxyfile COMMENT "Create Source documentation")
	add_custom_target(doc_api ${DOXYGEN} ${PROJECT_BINARY_DIR}/doc/Doxyfile_API_only COMMENT "Create API documentation")
	
	# Set the targets label in IDEs
	set_target_properties(doc PROPERTIES PROJECT_LABEL "Ptex Documentation (Full Source)")	
	set_target_properties(doc_api PROPERTIES PROJECT_LABEL "Ptex Documentation (API only)")	
	
	# The "${CMAKE_BINARY_DIR}/doc/ptex" is specified as the OUTPUT_DIRECTORY variable in the Doxyfile.
	file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/doc/ptex)	
	# The "${CMAKE_BINARY_DIR}/doc/apidocs" is specified as the OUTPUT_DIRECTORY variable in the Doxyfile_API_only.
	file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/doc/apidocs)
	
	# Install the uvellipse file.
	install(FILES ${PROJECT_SOURCE_DIR}/doc/uvellipse.png DESTINATION doc/apidocs)
	install(FILES ${PROJECT_SOURCE_DIR}/doc/uvellipse.png DESTINATION doc/ptex)
	
    install(DIRECTORY ${CMAKE_BINARY_DIR}/doc/ptex
            DESTINATION doc
            FILES_MATCHING PATTERN "*")	
    install(DIRECTORY ${CMAKE_BINARY_DIR}/doc/apidocs
            DESTINATION doc
            FILES_MATCHING PATTERN "*")	            		
else()
	message("You won't be able to build the documentation because 'doxygen' could not be found.")
endif()