MACRO(PARSE_ARGUMENTS prefix arg_names option_names)
  SET(DEFAULT_ARGS)
  FOREACH(arg_name ${arg_names})    
    SET(${prefix}_${arg_name})
  ENDFOREACH(arg_name)
  FOREACH(option ${option_names})
    SET(${prefix}_${option} FALSE)
  ENDFOREACH(option)

  SET(current_arg_name DEFAULT_ARGS)
  SET(current_arg_list)
  FOREACH(arg ${ARGN})            
    SET(larg_names ${arg_names})    
    LIST(FIND larg_names "${arg}" is_arg_name)                   
    IF (is_arg_name GREATER -1)
      SET(${prefix}_${current_arg_name} ${current_arg_list})
      SET(current_arg_name ${arg})
      SET(current_arg_list)
    ELSE (is_arg_name GREATER -1)
      SET(loption_names ${option_names})    
      LIST(FIND loption_names "${arg}" is_option)            
      IF (is_option GREATER -1)
	     SET(${prefix}_${arg} TRUE)
      ELSE (is_option GREATER -1)
	     SET(current_arg_list ${current_arg_list} ${arg})
      ENDIF (is_option GREATER -1)
    ENDIF (is_arg_name GREATER -1)
  ENDFOREACH(arg)
  SET(${prefix}_${current_arg_name} ${current_arg_list})
ENDMACRO(PARSE_ARGUMENTS)

MACRO(CAR var)
  SET(${var} ${ARGV1})
ENDMACRO(CAR)

MACRO(CDR var junk)
  SET(${var} ${ARGN})
ENDMACRO(CDR)


MACRO(MAKE_WS)
  PARSE_ARGUMENTS(WS "NAME;SOURCES;LIBS" "FCGI;ISAPI;DUMMY;QT" ${ARGN})
  CAR(WS_NAME ${WS_DEFAULT_ARGS})
  CDR(WS_SOURCES ${WS_DEFAULT_ARGS})
  
  IF(WS_FCGI)
    #ADD_DEFINITIONS(-DWS_TYPE=1)
    MESSAGE("Cr�ation du webservice ${WS_NAME} en FastCGI")
  ELSEIF(WS_ISAPI)
    #ADD_DEFINITIONS(-DWS_TYPE=2)
    MESSAGE("Cr�ation du webservice ${WS_NAME} en ISAPI")
  ELSEIF(WS_DUMMY)
    #ADD_DEFINITIONS(-DWS_TYPE=3)
    MESSAGE("Cr�ation du webservice ${WS_NAME} en DUMMY")
  ELSEIF(WS_QT)
    MESSAGE("Cr�ation du webservice ${WS_NAME} en Qt")
  ELSE(WS_FCGI)
    IF(WIN32)
      #ADD_DEFINITIONS(-DWS_TYPE=2)
      SET(WS_ISAPI TRUE)
      MESSAGE("Cr�ation du webservice ${WS_NAME} en ISAPI (choix par d�faut)")
    ELSE(WIN32)
      #ADD_DEFINITIONS(-DWS_TYPE=1)
      SET(WS_FCGI TRUE)
      MESSAGE("Cr�ation du webservice ${WS_NAME} en FastCGI (choix par d�faut)")
    ENDIF(WIN32)
  ENDIF(WS_FCGI)
    
  FIND_PACKAGE(Boost 1.40.0 COMPONENTS system thread REQUIRED)
  link_directories (${Boost_LIBRARY_DIRS})
  include_directories (${Boost_INCLUDE_DIRS})
  SET(WS_SOURCES ${WS_SOURCES} ${CMAKE_SOURCE_DIR}/WS_commons/configuration.cpp ${CMAKE_SOURCE_DIR}/WS_commons/configuration.h ${CMAKE_SOURCE_DIR}/WS_commons/data_structures.h ${CMAKE_SOURCE_DIR}/WS_commons/data_structures.cpp)
  IF(WS_FCGI)
    FIND_PACKAGE(fcgi REQUIRED)
    link_directories (${FCGI_LIBRARY_DIRS})
    include_directories (${CMAKE_SOURCE_DIR}/WS_commons ${FCGI_INCLUDE_DIRS})
    add_executable(${WS_NAME} ${WS_SOURCES})
    target_link_libraries(${WS_NAME} ${WS_LIBS} ${FCGI_LIBRARY} ${Boost_LIBRARIES} readline)
	SET_TARGET_PROPERTIES(${WS_NAME} PROPERTIES COMPILE_FLAGS -DWS_TYPE=1)
  ELSEIF(WS_ISAPI)
    FIND_LIBRARY(LIB_WS2 Ws2_32  REQUIRED)
    include_directories (${CMAKE_SOURCE_DIR}/WS_commons)
    add_library(${WS_NAME} SHARED ${WS_SOURCES} ${CMAKE_SOURCE_DIR}/WS_Commons/export.def)
	SET_TARGET_PROPERTIES(${WS_NAME} PROPERTIES COMPILE_FLAGS -DWS_TYPE=2)
    IF(MSVC)
      target_link_libraries(${WS_NAME} ${WS_LIBS})
    ELSE(MSVC)
      target_link_libraries(${WS_NAME} ws2_32 ${WS_LIBS} ${Boost_LIBRARIES})
    ENDIF(MSVC)
  ELSEIF(WS_QT)
    FIND_PACKAGE(Qt4 REQUIRED)
    include(${QT_USE_FILE})
    QT4_WRAP_UI(qt_UI ${CMAKE_SOURCE_DIR}/WS_commons/qt/mainwindow.ui)
    QT4_WRAP_CPP(qt_MOC ${CMAKE_SOURCE_DIR}/WS_commons/qt/mainwindow.h)
    add_executable(${WS_NAME} ${WS_SOURCES} ${qt_UI} ${qt_MOC} ${CMAKE_SOURCE_DIR}/WS_commons/qt/main.h)
    INCLUDE_DIRECTORIES(${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_SOURCE_DIR}/WS_commons)
    IF(MSVC)
          target_link_libraries(${WS_NAME} ${QT_LIBRARIES} ${WS_LIBS})
    ELSE(MSVC)
          target_link_libraries(${WS_NAME} ${QT_LIBRARIES} ${WS_LIBS} ${Boost_LIBRARIES})
    ENDIF(MSVC)
    SET_TARGET_PROPERTIES(${WS_NAME} PROPERTIES COMPILE_FLAGS -DWS_TYPE=4)
  ENDIF(WS_FCGI)
  
ENDMACRO(MAKE_WS)
