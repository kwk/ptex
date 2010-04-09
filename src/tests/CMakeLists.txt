option(BUILD_TESTS "Build test programs?" ON)
if(BUILD_TESTS)
    message(STATUS "Tests will be built.")
	
    # Copy validation data to binary (not execution) directory. Execution directory would be ${CMAKE_BINARY_DIR}/tests
    configure_file(${CMAKE_SOURCE_DIR}/tests/ftestok.dat ${CMAKE_BINARY_DIR}/bin/ftestok.dat COPYONLY ESCAPE_QUOTES)
    configure_file(${CMAKE_SOURCE_DIR}/tests/rtestok.dat ${CMAKE_BINARY_DIR}/bin/rtestok.dat COPYONLY ESCAPE_QUOTES)
    configure_file(${CMAKE_SOURCE_DIR}/tests/run_tests.py ${CMAKE_BINARY_DIR}/bin/run_tests.py COPYONLY ESCAPE_QUOTES)
	
    # Specify a list of test binaries that shall be build
    set(testbins wtest rtest ftest halftest)

    #Make Ptex source files available for include in this project
    include_directories(${CMAKE_SOURCE_DIR}/ptex)

    # Iterate over every test binary
    foreach(testbin ${testbins})
	    add_executable(${testbin} ${testbin}.cpp)
	    prefix_hack(${testbin})
	    set_target_properties(${testbin} PROPERTIES DEBUG_POSTFIX "${debug_suffix}")
	    target_link_libraries(${testbin} ${libs} ptex)
	    set_target_properties(${testbin} PROPERTIES PROJECT_LABEL "Ptex Test (${testbin})")
	    install(TARGETS ${testbin} RUNTIME DESTINATION bin)
    endforeach()
   
    find_package(PythonInterp REQUIRED)
    add_custom_target(run_tests
                    COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_BINARY_DIR}/bin/run_tests.py
                    DEPENDS ${testbins}
                    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
                    COMMENT "Run tests")
    set_target_properties(run_tests PROPERTIES PROJECT_LABEL "Ptex RUN_TESTS")
    
    install(FILES
                ${CMAKE_SOURCE_DIR}/tests/rtestok.dat
                ${CMAKE_SOURCE_DIR}/tests/ftestok.dat
                ${CMAKE_SOURCE_DIR}/tests/run_tests.py
            DESTINATION bin)
           
else()
    message(Tests are not build)
endif()



