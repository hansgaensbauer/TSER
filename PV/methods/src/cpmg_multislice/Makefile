# -------------------------------------------------------------
# /pvVersion/360.2.0/install/prog/parx/src/cpmg_multislice/Makefile
# 
# Copyright (c) 2001-2018
# Bruker BioSpin MRI GmbH
# D-76275 Ettlingen, Germany
#
# All Rights Reserved
#
# To copy the directory and compile the copy it is only
# necessary to change SRCDIR.
# -------------------------------------------------------------


 #ifndef /pvVersion/360.2.0/thirdparty/toolchain/linux/zlib-1.2.11
 #  define /pvVersion/360.2.0/thirdparty/toolchain/linux/zlib-1.2.11 $(BUILD_TOOL_ROOT)/zlib
 #endif

M4_ROOT = /pvVersion/360.2.0/thirdparty/toolchain/linux/m4-1.4.18

TAR_ROOT = /pvVersion/360.2.0/thirdparty/toolchain/linux/tar-1.29

DVD_TOOLS_ROOT = /pvVersion/360.2.0/thirdparty/toolchain/linux/dvd-rw-tools-7.1-gcc-5.4.0

CDRKIT_ROOT = /pvVersion/360.2.0/thirdparty/toolchain/linux/cdrkit-svn860

DEFAULT_SYMBOL_VISIBILITY = -fvisibility=hidden

PROGLIBLDFLAGS = $(CC_EXEC_PREFIX_OPTION) $(PT_GNU_RELRO) $(PV_COMPILE_FLAGS) $(COMMON_FLAG) -fno-gnu-unique -fexceptions $(LINK_OPTIONS)

NLOPT_ROOT	= /pvVersion/360.2.0/thirdparty/toolchain/linux/nlopt-2.5.0

TCL_SHELL_ROOT	= /pvVersion/360.2.0/thirdparty/toolchain/linux/tcl-8.6.9

BISON_ROOT	= /pvVersion/360.2.0/thirdparty/toolchain/linux/bison-3.0.4

NO_LINKTIME_OPTIMIZE = -fno-lto

PT_GNU_RELRO	= -z relro -z now

CC_ROOT		= $(EXECDISKUNIT)/gnu

POCO_ROOT	= /pvVersion/360.2.0/thirdparty/toolchain/linux/poco-1.9.2-gcc-5.4.0

PIC_FLAG	= -fPIC

COMMON_FLAG	= -fno-common

EXCEPTION_FLAG	= -fexceptions

CC_EXEC_PREFIX_OPTION	= -B $(CC_ROOT)/lib/gcc

STDCXX_FLAGS	= -std=c++14

.SUFFIXES:            # Delete the default suffixes

tests::

GLOBAL_BUILD_TOOL_ROOT = /usr/$(LOCAL)

OS_ARTIFACTS_DIR = $(ARTIFACTS_DIR)/linux

WARN_AS_ERROR = -Werror

WARN_LINK_AS_ERROR = -Wl,--fatal-warnings

XWINSHLIBDIR = $(PROGDIR)/shlib
XWINSHLIBDIROPT = -L$(XWINSHLIBDIR)

THIRDPARTY_SHLIBDIR = $(PROGDIR)/pvshlib
THIRDPARTY_SHLIBDIROPT = -L$(THIRDPARTY_SHLIBDIR)

XWINSHARELIBEXT = $(SHARELIBEXT)

PVSHLIBDIR = $(PROGDIR)/pvshlib

RMD		= rm -rf

SHARELIBBASEOPTS = -shared

PV_EXTRA_DEFINES =

PV_DEFINES = -D_REENTRANT -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE

PV_ARCH_FLAG = -m64

PV_COMPILE_FLAGS = $(DEFAULT_SYMBOL_VISIBILITY) $(PV_ARCH_FLAG) $(PIC_FLAG) -rdynamic

CREATE_LINK_LIST = $(PERL)  $(PROGDIR)/bin/createLinkList.pl

MAKEFILE_DEP = $(SRCDIR)/Makefile

DEPDIR = depdir

AWK		= awk

BASENAME	= basename

BASH		= bash

CAT		= cat

CC		= LD_LIBRARY_PATH=$(CC_ROOT)/lib64 $(CC_ROOT)/bin/gcc -B$(CC_ROOT)/lib/gcc/

CHMOD		= chmod

CHOWN		= chown

CKSUM		= cksum

CMP		= cmp

CP		= cp --remove-destination --update -p

CP_R		= cp -ax

CPASC		= cp --remove-destination --update -p

CUT		= cut

DATE		= date

DIFF		= diff

DIRNAME		= dirname

DOS2UNIX	= dos2unix

ECHO		= /bin/echo -e

FIND		= find

GREP		= grep

HEAD		= head

IMAKE_ROOT	= /pvVersion/360.2.0/thirdparty/toolchain/linux/imake-1.0.7

IMAKE_CPP	= $(CPP)

LN		= ln -f

LS		= ls

MAKE_ROOT	= /pvVersion/360.2.0/thirdparty/toolchain/linux/make-4.2.1.pv

MAKE		= make

MD5SUM		= md5sum

MKDIR		= mkdir -p

MV		= mv -f

NM		= nm

NOOP		= true

PERL_ROOT	= /pvVersion/360.2.0/thirdparty/toolchain/linux/perl-5.26.2

PERL		= $(EXECDISKUNIT)/perl/bin/perl -I$(PROGDIR)/perl

RCP		= rcp

READLINK	= readlink

RM		= rm -f --

RMDIR		= rm -rf

RSYNC	= rsync -a --no-owner

SCP		= scp

SED		= sed

SED_OPT_INPLACE	= -i

SHARELIBCMD	=

SHELL		= sh

TOUCH		= touch

UNAME		= uname

WHOAMI		= whoami

NOOP		= true

STRIP		= $(CC_ROOT)/bin/strip

SORT		= sort -u

DOS2UNIX	= dos2unix

SSH		= ssh

COMM		= comm

NM		= nm

ZIPCMD		= gzip -f

UNZIPCMD	= gunzip -f

SUDO	= /usr/bin/sudo -n

READLINK	= readlink

TOP		= .
CURRENT_DIR	= .

RM_CMD		= $(RM) *.CKP *.ln *.BAK *.bak *.o core errs ,* *~ *.a *.lib .emacs_* tags TAGS make.log MakeOut

APP_SUBSYSTEM	=

STD_LIBRARIES	= -ldl -lrt -lpthread $(EXTRA_STDLIBS)
ALL_LIBRARIES	= $(LIBRARIES) $(EXTRA_LIBRARIES) $(STD_LIBRARIES)

STD_LIBPATH	=
ALL_LIBPATH	= $(LIBPATH) $(STD_LIBPATH)

STD_INCPATH	= -I $(GLOBALHEADERDIR)
ALL_INCPATH	= $(INCPATH) $(EXTRA_INCPATH) $(STD_INCPATH)

STD_DEFINES	= -D_REENTRANT -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE
OS_DEFINES	= -DLINUX_INTEL
DLL_DEFINES	=
ALL_DEFINES	= $(OS_DEFINES) $(DEFINES) $(EXTRA_DEFINES) $(DLL_DEFINES) $(STD_DEFINES)

CDEBUGFLAGS	= -O2 -DNDEBUG $(LINKTIME_OPTIMIZE)

CCOPTIONS	= $(CC_EXEC_PREFIX_OPTION) $(PV_COMPILE_FLAGS) $(COMMON_FLAG) -Wall -Wextra $(WARN_AS_ERROR) -Wcast-qual -Wpointer-arith -Wsign-compare -Wwrite-strings -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations -Wnested-externs -Winline -Wdisabled-optimization -Waggressive-loop-optimizations -Wlogical-op -Wconversion -Wcast-align -pedantic -std=gnu99 -fexceptions $(COMPILE_OPTIONS)

CCLDOPTIONS	= $(CC_EXEC_PREFIX_OPTION) $(PT_GNU_RELRO) -O2 $(LINKTIME_OPTIMIZE) $(PV_COMPILE_FLAGS) $(COMMON_FLAG) -fno-gnu-unique -fexceptions $(LINK_OPTIONS)

STATICLIBGCC	= -static-libgcc

LDDEBUGFLAGS	=

LDOPTIONS	=

DLLLDOPTIONS	=

CFLAGS		= $(CDEBUGFLAGS) $(CCOPTIONS) $(ALL_INCPATH) $(ALL_DEFINES)
CCLDFLAGS	= $(CDEBUGFLAGS) $(CCOPTIONS) $(CCLDOPTIONS) $(ALL_LIBPATH)

EXECEXT		=

OBJEXT		= .o

STATICLIBEXT	= .a

STATICCRTLIBEXT	= .a

DYNAMICLIBEXT	= .so

ASMEXT		= .asm

ROMEXT		= .rom

ZIPEXT		= .gz

SHARELIBEXT	= .so

BOOST_LIBRARYPATH = $(SHLIBDIR)
BOOST_INCPATH	= -isystem $(GLOBALHEADERDIR)/$(notdir /pvVersion/360.2.0/thirdparty/toolchain/linux/boost-1.64.0-gcc-5.4.0)/include

GTEST_LIBRARIES	= $(GTEST_ROOT)/lib/gtest_main.a
GTEST_INCPATH	= -isystem $(GTEST_ROOT)/include

IDL_BASE_STATICLIBRARIES = $(OMNI_ROOT)/lib/libomniORB4.a $(OMNI_ROOT)/lib/libomniCodeSets4.a $(OMNI_ROOT)/lib/libomnithread.a $(OMNI_ROOT)/lib/libomnisslTP4.a $(SSL_BASE_STATICLIBRARIES)

NLOPT_LIBRARIES	= $(NLOPT_ROOT)/lib64/libnlopt.a
NLOPT_INCPATH	= -isystem $(NLOPT_ROOT)/include

POCO_LIBRARIES	= $(POCO_ROOT)/lib/libPocoData.so $(POCO_ROOT)/lib/libPocoDataSQLite.so $(POCO_ROOT)/lib/libPocoEncodings.so $(POCO_ROOT)/lib/libPocoMongoDB.so $(POCO_ROOT)/lib/libPocoNet.so $(POCO_ROOT)/lib/libPocoRedis.so $(POCO_ROOT)/lib/libPocoZip.so $(POCO_ROOT)/lib/libPocoNetSSL.so $(POCO_ROOT)/lib/libPocoUtil.so $(POCO_ROOT)/lib/libPocoCrypto.so $(POCO_ROOT)/lib/libPocoXML.so $(POCO_ROOT)/lib/libPocoJSON.so $(POCO_ROOT)/lib/libPocoFoundation.so $(SSL_LIBRARIES)
POCO_STATICLIBRARIES = $(POCO_ROOT)/lib/libPocoData.a $(POCO_ROOT)/lib/libPocoDataSQLite.a $(POCO_ROOT)/lib/libPocoEncodings.a $(POCO_ROOT)/lib/libPocoMongoDB.a $(POCO_ROOT)/lib/libPocoRedis.a $(POCO_ROOT)/lib/libPocoZip.a $(POCO_ROOT)/lib/libPocoNetSSL.a $(POCO_ROOT)/lib/libPocoNet.a $(POCO_ROOT)/lib/libPocoUtil.a $(POCO_ROOT)/lib/libPocoCrypto.a $(POCO_ROOT)/lib/libPocoXML.a $(POCO_ROOT)/lib/libPocoJSON.a $(POCO_ROOT)/lib/libPocoFoundation.a $(SSL_STATICLIBRARIES)
POCO_DEFINES	=
POCO_INCPATH	= -isystem $(POCO_ROOT)/include $(SSL_INCPATH)

SSL_BASE_STATICLIBRARIES = $(SSL_ROOT)/lib/libssl.a $(SSL_ROOT)/lib/libcrypto.a

MATH_LIBRARIES	= -lm

FILESYSTEM_LIBRARIES = -lstdc++fs

FORTRAN_LIBRARIES = -lgfortran

PTHREAD_LIBRARIES = -lpthread

RT_LIBRARIES	= -lrt

EXECDISKUNIT	= /opt/PV-360.2.0.pl.1

PROGDIR		= $(EXECDISKUNIT)/prog

STANDALONEDIR	= $(EXECDISKUNIT)/prog/bin

DLLDIR		= $(PROGDIR)/pvshlib

SHLIBDIR	= $(PROGDIR)/pvshlib

GLOBALHEADERDIR	= $(PROGDIR)/include

COMMONCONFIGDIR	= $(TS_IMPORT_DIR)/bscl/gen/config

TMPDIR		= /tmp

DEPENDFLAGS	= -MT $@ -MD -MP -MF $(DEPDIR)/$(@F:$(OBJEXT)=.Td)

CPLUSPLUS		= LD_LIBRARY_PATH=$(CC_ROOT)/lib64 $(CC_ROOT)/bin/c++ -B$(CC_ROOT)/lib/gcc/

STD_PLUSPLUS_LIBRARIES	= -ldl -lrt -lpthread $(EXTRA_STDLIBS)
ALL_PLUSPLUS_LIBRARIES	= $(LIBRARIES) $(EXTRA_LIBRARIES) $(STD_PLUSPLUS_LIBRARIES)

STD_PLUSPLUS_LIBPATH 	=
ALL_PLUSPLUS_LIBPATH	= $(LIBPATH) $(STD_PLUSPLUS_LIBPATH)

STD_PLUSPLUS_INCPATH 	= $(STD_INCPATH)
ALL_PLUSPLUS_INCPATH	= $(INCPATH) $(EXTRA_INCPATH) $(STD_PLUSPLUS_INCPATH)

STATICSTDCPLUSPLUS	= -static-libgcc -static-libstdc++

SHAREDSTDCPLUSPLUS	= libgcc_s.so.1 libstdc++.so.6

STD_PLUSPLUS_DEFINES 	= -D_REENTRANT -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE
ALL_PLUSPLUS_DEFINES	= $(OS_DEFINES) $(DEFINES) $(EXTRA_DEFINES) $(DLL_DEFINES) $(STD_PLUSPLUS_DEFINES)

CPLUSPLUSDEBUGFLAGS	= -O2 -DNDEBUG $(LINKTIME_OPTIMIZE)

CPLUSPLUSOPTIONS	= -x c++ $(CC_EXEC_PREFIX_OPTION) $(PV_COMPILE_FLAGS) $(STDCXX_FLAGS) -Wall -Wextra $(WARN_AS_ERROR) -Weffc++ -Wcast-qual -Wpointer-arith -Wsign-compare -Wundef -Wdisabled-optimization -Waggressive-loop-optimizations -Wshadow -Wlogical-op -Woverloaded-virtual -Wwrite-strings -Wmissing-declarations -Wcast-qual -Wcast-align -Wno-variadic-macros -Wno-long-long -Wstrict-null-sentinel $(COMMON_FLAG) -fimplicit-templates -fnon-call-exceptions  $(COMPILE_OPTIONS) -fvisibility-inlines-hidden
CPLUSPLUSLDOPTIONS	= $(CC_EXEC_PREFIX_OPTION) $(PT_GNU_RELRO) -O2 $(LINKTIME_OPTIMIZE) $(PV_COMPILE_FLAGS) $(COMMON_FLAG) -fno-gnu-unique -fexceptions $(LINK_OPTIONS)

CPLUSPLUSFLAGS		= $(CPLUSPLUSDEBUGFLAGS) $(CPLUSPLUSOPTIONS) $(ALL_PLUSPLUS_INCPATH) $(ALL_PLUSPLUS_DEFINES)

CPLUSPLUSLDFLAGS	= $(CPLUSPLUSLDOPTIONS) $(ALL_PLUSPLUS_LIBPATH)

PLUSPLUSDEPENDFLAGS 	= -MT $@ -MD -MP -MF $(DEPDIR)/$(@F:$(OBJEXT)=.Td)

PLUSPLUSDEPEND		= Depend

PPSUFFIX		= .cc

$(DEPDIR):
	$(MKDIR) $(DEPDIR)

define CREATE_SIMPLE_DEPS

$1 : $3/$(notdir $(1:$(OBJEXT)=$2)) $(DEPDIR)/$(notdir $(1:$(OBJEXT)=.d)) | $(DEPDIR)
$(DEPDIR)/$(notdir $(1:$(OBJEXT)=.d)): ;

endef

clean:: depdirclean

depdirclean: | $(DEPDIR)
	$(RM) $(addsuffix *.d,$(DEPDIR)/)

define INSTALL_FILES_FCN
install:: $$(strip $(2))
$$(strip $(2)) : $(1) | $$(abspath $$(dir $(2)))
	$(RM) $(2)
	$(CP) $(1) $(2)

clean::
	$(RM) $2
endef

define INSTALL_ASCII_FILES_FCN
install:: $$(strip $(2))
$$(strip $(2)) : $(1) | $$(abspath $$(dir $(2)))
	$(RM) $(2)
	$(CPASC) $(1) $(2)

clean::
	$(RM) $2
endef

define COPY_TARGET
$(eval $(call MKDIR_FCN,$$(abspath $$(dir $2))))
$2 : $1 | $$(abspath $$(dir $2))
	$$(info Copy $1 to $2)
	$$(RM) $2
	$$(CP) $1 $2

clean::
	$$(RM) $2

endef

define MKDIR_FCN

ifeq ($$(filter $(1),$$(PV_CREATE_DIRS)),)
PV_CREATE_DIRS += $(1)

$$(strip $(1)):
	$$(MKDIR) $(1)

endif
endef

.PHONY : all clean depend dll docu dvd emptyrule idl install release test

DEPEND_START = \# DO NOT DELETE THIS LINE -- make depend depends on it

TEST_LABEL	= test

test:: test_exec

test test_exec:: test_build

test_build::

STD_FORTRAN_LIBRARIES	= -ldl -lrt -lpthread $(EXTRA_STDLIBS)

ALL_FORTRAN_LIBRARIES	= $(LIBRARIES) $(EXTRA_LIBRARIES) $(STD_FORTRAN_LIBRARIES)

SIMPLE_FORTRAN_LIBRARIES = -lgfortran

STD_FORTRAN_LIBPATH 	=
ALL_FORTRAN_LIBPATH	= $(LIBPATH) $(STD_FORTRAN_LIBPATH)

STD_FORTRAN_INCPATH 	= -I $(GLOBALHEADERDIR)
ALL_FORTRAN_INCPATH	= $(INCPATH) $(EXTRA_INCPATH) $(STD_FORTRAN_INCPATH)

STATICSTDFORTRAN	= -static

STD_FORTRAN_DEFINES 	= -D_REENTRANT -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE
ALL_FORTRAN_DEFINES	= $(OS_DEFINES) $(DEFINES) $(EXTRA_DEFINES) $(DLL_DEFINES) $(STD_FORTRAN_DEFINES)

FORTRANDEBUGFLAGS	= -O2 -DNDEBUG $(LINKTIME_OPTIMIZE) -std=legacy -fdefault-integer-8 -frecord-marker=8 -ffast-math -fstrict-aliasing -funroll-all-loops

FORTRANNOOPTDEBUGFLAGS	= -fPIC -DNDEBUG -std=legacy -fdefault-integer-8 -frecord-marker=8

FORTRANOPTIONS		= $(CC_EXEC_PREFIX_OPTION) $(PV_COMPILE_FLAGS) -Wall -W -Winline -Wdisabled-optimization $(COMPILE_OPTIONS) -Wno-compare-reals -Wno-conversion -Wno-unused -Wno-unused-parameter -Wno-unused-dummy-argument -Wno-intrinsic-shadow -Wno-intrinsics-std -Wno-conversion-extra -Wno-surprising -Wno-maybe-uninitialized -Wno-unused-but-set-variable -Wno-unused-variable

FORTRANLDOPTIONS	= $(CC_EXEC_PREFIX_OPTION) $(PT_GNU_RELRO) -O2 $(LINKTIME_OPTIMIZE) $(PV_COMPILE_FLAGS) $(COMMON_FLAG) -fno-gnu-unique -fexceptions $(LINK_OPTIONS)

FORTRANFLAGS		= $(FORTRANDEBUGFLAGS) $(FORTRANOPTIONS) $(ALL_FORTRAN_INCPATH) $(ALL_FORTRAN_DEFINES)

FORTRANNOOPTFLAGS	= $(FORTRANNOOPTDEBUGFLAGS) $(FORTRANOPTIONS) $(ALL_FORTRAN_INCPATH) $(ALL_FORTRAN_DEFINES)

FORTRANLDFLAGS	= $(FORTRANLDOPTIONS) $(ALL_FORTRAN_LIBPATH)

FORTRANDEPENDFLAGS 	= -MD -MP -MF $(DEPDIR)/$(@F:$(OBJEXT)=.Td) -cpp

FORTRANDEPEND		= Depend

FSUFFIX			= .f

LAPACK_DIR = /pvVersion/360.2.0/thirdparty/toolchain/linux/lapack
LAPACK_COPYLIBS = $(LAPACK_DIR)/lib64/liblapack.so.3 $(LAPACK_DIR)/lib64/libblas.so.3
LAPACK_LIBRARIES = $(LAPACK_DIR)/lib64/liblapack$(SHARELIBEXT) $(LAPACK_DIR)/lib64/libblas$(SHARELIBEXT) $(SIMPLE_FORTRAN_LIBRARIES)

PARCOMP_OPTS     =
PARCOMP_DEFINES  = -DInParxOvl
PARCOMP_DEPENDFLAGS = -d -MT,$@,-MD,-MP,-MF,$(DEPDIR)/$(basename $(@F)).Td
PARCOMP_FLAGS	 = $(PARCOMP_DEPENDFLAGS) $(PARX_EXTRA_FLAGS) -I. $(ALL_INCPATH) $(DEFINES) $(PARCOMP_DEFINES) $(PARCOMP_OPTS) $(PARCOMP_DEBUG)
PARCOMP_DEBUG    =
PARCOMP	         = $(PROGDIR)/bin/scripts/methcomp

PARX_OVL_LIBPATH = -L$(SHLIBDIR) -L$(XWINSHLIBDIR)
PARX_OVL_LIBS	 = $(LIBS)
PARX_OVL_LIBRARIES = $(LIBRARIES) $(STD_LIBRARIES)
PARX_OVL_LD      = LD_LIBRARY_PATH=$(CC_ROOT)/lib64 $(CC_ROOT)/bin/c++ -B$(CC_ROOT)/lib/gcc/
PARX_OVL_EXT     = $(SHARELIBEXT)
PARX_OVL_DEF_EXT = .ovl
PARX_OVL_EXT_EXT = .def
PARX_OVL_AR      = $(AR)
PARX_OVL_ARFLAGS =
PARX_TB_EXT      = $(SHARELIBEXT)
PARX_TB_DEF_EXT  = .c

PARX_TOOLBOX_DIR = $(DLLDIR)
METHODS_DIR	 = $(EXECDISKUNIT)/prog/curdir/nmrsu/ParaVision/methods
METHODS_SRC_DIR  = $(PROGDIR)/parx/src
STD_COMMON_METHOD_LIBS = \
$(SHLIBDIR)/libPvCfgTools$(SHARELIBEXT) \
$(SHLIBDIR)/libPvPvmTools$(SHARELIBEXT) \
$(SHLIBDIR)/libPvUtilTools$(SHARELIBEXT) \
$(SHLIBDIR)/libPvGeoTools$(SHARELIBEXT) \
$(SHLIBDIR)/libPvSeqTools$(SHARELIBEXT) \
$(SHLIBDIR)/libPvOvlTools$(SHARELIBEXT) \
$(SHLIBDIR)/libAtsProperties$(SHARELIBEXT) \
$(SHLIBDIR)/libModality$(SHARELIBEXT) \
$(SHLIBDIR)/libPvAdj$(SHARELIBEXT) \
$(SHLIBDIR)/libLicenseService$(SHARELIBEXT) \
$(SHLIBDIR)/libLogService$(SHARELIBEXT) \
$(SHLIBDIR)/libCommonConfiguration$(SHARELIBEXT) \
$(SHLIBDIR)/libParxRels$(SHARELIBEXT) \
$(SHLIBDIR)/libParxBase$(SHARELIBEXT) \
$(SHLIBDIR)/libParxUtils$(SHARELIBEXT) \
$(SHLIBDIR)/libPvDatabase$(SHARELIBEXT) \
$(SHLIBDIR)/libPvVersion$(SHARELIBEXT) \
$(SHLIBDIR)/libPvUtil$(SHARELIBEXT) \
$(SHLIBDIR)/libPluma$(SHARELIBEXT) \
$(SHLIBDIR)/libPvnl$(SHARELIBEXT) \
$(SHLIBDIR)/libPvnlFT$(SHARELIBEXT) \
$(SHLIBDIR)/libimproc$(SHARELIBEXT) \
$(SHLIBDIR)/libCmd$(SHARELIBEXT) \
$(SHLIBDIR)/libCmdBase$(SHARELIBEXT) \
$(SHLIBDIR)/libCoreMisc$(SHARELIBEXT) \
$(SHLIBDIR)/libCoreThread$(SHARELIBEXT) \
$(SHLIBDIR)/libCoreCommon$(SHARELIBEXT) \
$(SHLIBDIR)/libCoreRemote$(SHARELIBEXT) \
$(SHLIBDIR)/libPvIdl$(SHARELIBEXT) \
$(SHLIBDIR)/libLogger$(SHARELIBEXT) \
$(SHLIBDIR)/libPvGeo$(SHARELIBEXT)

PARX_OVL_MODALITY = MR

PARX_OVL_PROG_LIBPATH =
PARX_OVL_PROG_LIBRARIES = -lomniCodeSets4 -lomnisslTP4  -lomniORB4 -lomnithread -lssl -lcrypto -lpthread -llapack -lblas -lgfortran -lm -lz

PARX_SCRIPTS_DIR = $(PROGDIR)/parx/scripts

EXTRA_DEFINES    = $(PARCOMP_DEFINES)

CPROTO_ROOT = /pvVersion/360.2.0/thirdparty/toolchain/linux/cproto-4.7l
CPROTO = $(PROGDIR)/bin/cproto
CPROTOOPTIONS   = -E"$(CC) $(CC_EXEC_PREFIX_OPTION) -E" -f2
CPROTO_DEFINES  = -DCPROTO -D__float128=double
CPROTOFLAGS     = $(CPROTOOPTIONS) $(CPROTO_DEFINES) $(ALL_DEFINES) $(subst -isystem, -I, $(ALL_INCPATH))
PARX_PROTOHEAD  = $(GLOBALHEADERDIR)/Parx/Rels/ParxProtoHead.h
PARX_PROTOFOOT  = $(GLOBALHEADERDIR)/Parx/Rels/ParxProtoFoot.h

EXP_LISTS_DIR    = $(EXPDIR)/stan/nmr/lists
PPG_DIR	 = $(EXECDISKUNIT)/prog/curdir/nmrsu/ParaVision/exp/lists/pp
PPG_INCPATH = -I $(PPG_DIR) -I $(EXP_LISTS_DIR)/pp -I $(EXP_LISTS_DIR)/pp.dexam
CREATE_PPG_ATTACHMENT = $(STANDALONEDIR)/createPpgAttachment
STD_MXI_METHOD_LIBS =  \
$(SHLIBDIR)/libRecoTools$(SHARELIBEXT)  \
$(SHLIBDIR)/libOvlUtil$(SHARELIBEXT)  \
$(SHLIBDIR)/libPvSysInfo$(SHARELIBEXT)  \
$(SHLIBDIR)/libReadParx$(SHARELIBEXT) \
$(SHLIBDIR)/libpvrouting$(SHARELIBEXT) \
$(XWINSHLIBDIR)/editpar$(XWINSHARELIBEXT)\
$(XWINSHLIBDIR)/libLog$(XWINSHARELIBEXT)\
$(XWINSHLIBDIR)/LogFile$(XWINSHARELIBEXT)\
$(XWINSHLIBDIR)/restartClient$(XWINSHARELIBEXT)\
$(XWINSHLIBDIR)/ServerTable$(XWINSHARELIBEXT)\
$(XWINSHLIBDIR)/Bis$(XWINSHARELIBEXT) \
$(XWINSHLIBDIR)/Language$(XWINSHARELIBEXT) \
$(XWINSHLIBDIR)/libcb$(XWINSHARELIBEXT) \
$(XWINSHLIBDIR)/libacq$(XWINSHARELIBEXT)     \
$(XWINSHLIBDIR)/libap$(XWINSHARELIBEXT)     \
$(XWINSHLIBDIR)/libCt$(XWINSHARELIBEXT)      \
$(XWINSHLIBDIR)/libHConfClient$(XWINSHARELIBEXT) \
$(XWINSHLIBDIR)/libReadConf$(XWINSHARELIBEXT) \
$(XWINSHLIBDIR)/libssc$(SHARELIBEXT) \
$(XWINSHLIBDIR)/libssi$(SHARELIBEXT) \
$(XWINSHLIBDIR)/convpw$(SHARELIBEXT) \
$(XWINSHLIBDIR)/libacu$(SHARELIBEXT) \
$(XWINSHLIBDIR)/libCube$(SHARELIBEXT) \
$(XWINSHLIBDIR)/librrs$(XWINSHARELIBEXT)     \
$(XWINSHLIBDIR)/Error$(SHARELIBEXT) \
$(XWINSHLIBDIR)/ipsoRout$(SHARELIBEXT) \
$(XWINSHLIBDIR)/libRfRouting$(XWINSHARELIBEXT) \
$(XWINSHLIBDIR)/libWobbleUtil$(XWINSHARELIBEXT) \
$(XWINSHLIBDIR)/BsclXml$(XWINSHARELIBEXT) \
$(XWINSHLIBDIR)/BsclThread$(XWINSHARELIBEXT)\
$(XWINSHLIBDIR)/libShapeIO$(XWINSHARELIBEXT) \
$(XWINSHLIBDIR)/BsclUtil$(XWINSHARELIBEXT)    \
$(XWINSHLIBDIR)/libCorbaTools$(XWINSHARELIBEXT)     \
$(XWINSHLIBDIR)/uni$(XWINSHARELIBEXT) \
$(XWINSHLIBDIR)/util$(XWINSHARELIBEXT) \
$(XWINSHLIBDIR)/libPath$(XWINSHARELIBEXT) \
$(XWINSHLIBDIR)/par$(XWINSHARELIBEXT)  \
$(XWINSHLIBDIR)/libCoToolServer$(XWINSHARELIBEXT) \
$(XWINSHLIBDIR)/libCoAcq$(XWINSHARELIBEXT)\
$(XWINSHLIBDIR)/libCoAcqCommon$(XWINSHARELIBEXT)\
$(XWINSHLIBDIR)/libCoSsi$(XWINSHARELIBEXT)\
$(XWINSHLIBDIR)/libCoData$(XWINSHARELIBEXT)\
$(XWINSHLIBDIR)/libCoSsiProbeAdmin$(XWINSHARELIBEXT)\
$(XWINSHLIBDIR)/libCoCpr$(XWINSHARELIBEXT)     \
$(XWINSHLIBDIR)/libCoGojava$(XWINSHARELIBEXT)\
$(XWINSHLIBDIR)/libCoIpsoRestart2$(XWINSHARELIBEXT)\
$(XWINSHLIBDIR)/libCoCommon$(XWINSHARELIBEXT) $(STD_COMMON_METHOD_LIBS)

STD_MR_METHOD_LIBS  = \
$(SHLIBDIR)/libPvMrAdj$(SHARELIBEXT) \
$(SHLIBDIR)/libPvCfgMR$(SHARELIBEXT) \
$(SHLIBDIR)/libPvMrTools$(SHARELIBEXT) \
$(SHLIBDIR)/libPvAcqToolsMr$(SHARELIBEXT) \
$(SHLIBDIR)/libPvCfgToolsMr$(SHARELIBEXT) \
$(SHLIBDIR)/libPvGeoToolsMr$(SHARELIBEXT) \
$(SHLIBDIR)/libPvPvmToolsMr$(SHARELIBEXT) \
$(SHLIBDIR)/libPvSeqToolsMr$(SHARELIBEXT) \
$(SHLIBDIR)/libPvOvlToolsMr$(SHARELIBEXT) \
$(SHLIBDIR)/libpvShimClient$(SHARELIBEXT) \
$(SHLIBDIR)/libPvGenericServer2MgrCommon$(SHARELIBEXT) \
$(SHLIBDIR)/libPvGenericServer2MgrMr$(SHARELIBEXT) $(STD_MXI_METHOD_LIBS)

.PHONY : cproto

.PHONY: instclean instlist

installppg :

.PHONY: forceppg

forceppg:

$(VERBOSE).SILENT:

all::
showppg ::
	@if [ -n "$(PULPROG)" -a "$(PULPROG)" != "none" ]; then echo $(notdir $(PULPROG)); fi

OVERLAY		= cpmg_multislice

SRCDIR		= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

OBJS		=	\
			initMeth$(OBJEXT) \
			loadMeth$(OBJEXT) \
			backbone$(OBJEXT) \
			parsRelations$(OBJEXT) \
			BaseLevelRelations$(OBJEXT) \
			RecoRelations$(OBJEXT) 

SRCS		= $(addprefix $(SRCDIR)/, $(addsuffix .c, $(basename $(notdir $(OBJS)))))

LIBS		= $(STD_MR_METHOD_LIBS)

all::	$(OVERLAY)$(PARX_OVL_EXT)

install_SUBDIRS:
$(SUBDIR_OBJS) : install_SUBDIRS
$(OVERLAY).objlist :  $(OVERLAY)$(OBJEXT) $(OBJS) $(SUBDIR_OBJS)
	$(RM) $(OVERLAY).objlist
	$(TOUCH) $(OVERLAY).objlist
	$(CREATE_LINK_LIST) -o $(OVERLAY).objlist $(OVERLAY)$(OBJEXT) $(OBJS) $(SUBDIR_OBJS)

clean::
	$(RM) $(OVERLAY).objlist

install:: $(OVERLAY)$(PARX_OVL_EXT)

$(foreach obj,$(notdir $(GLOBALHEADERDIR)/Parx/Rels/_ParxMain)$(OBJEXT),$(eval $(call CREATE_SIMPLE_DEPS,$(obj),$(PPSUFFIX), $(dir $(GLOBALHEADERDIR)/Parx/Rels/_ParxMain))))

$(notdir $(GLOBALHEADERDIR)/Parx/Rels/_ParxMain)$(OBJEXT): | $(DEPDIR)
	$(info Compile  $(dir $(GLOBALHEADERDIR)/Parx/Rels/_ParxMain)/$(@F:$(OBJEXT)=$(PPSUFFIX)))
	$(CPLUSPLUS) $(PLUSPLUSDEPENDFLAGS) $(CPLUSPLUSFLAGS) -c  $(dir $(GLOBALHEADERDIR)/Parx/Rels/_ParxMain)/$(@F:$(OBJEXT)=$(PPSUFFIX)) &&\
	$(MV) $(DEPDIR)/$(@F:$(OBJEXT)=.Td) $(DEPDIR)/$(@F:$(OBJEXT)=.d) && touch $@
-include $(addprefix $(DEPDIR)/,$(addsuffix .d,$(basename $(notdir $(notdir $(GLOBALHEADERDIR)/Parx/Rels/_ParxMain)$(OBJEXT)))))

$(OVERLAY)$(PARX_OVL_EXT):  $(notdir $(GLOBALHEADERDIR)/Parx/Rels/_ParxMain)$(OBJEXT) $(PARX_OVL_LIBS) $(OVERLAY).objlist
	$(info Link $(OVERLAY)$(PARX_OVL_EXT))
	$(RM) $(OVERLAY)$(PARX_OVL_EXT)
	$(RM) $(OVERLAY).program
	$(MKDIR) $(join link_,$(OVERLAY))
	TMPDIR=$(join link_,$(OVERLAY)) $(PARX_OVL_LD) $(PROGLIBLDFLAGS)  $(notdir $(GLOBALHEADERDIR)/Parx/Rels/_ParxMain)$(OBJEXT) @$(OVERLAY).objlist \
	  $(PARX_OVL_LIBPATH) $(PARX_OVL_PROG_LIBPATH) $(PARX_OVL_LIBS) $(PARX_OVL_LIBRARIES) $(PARX_OVL_PROG_LIBRARIES) \
	  -o $(OVERLAY).program
	$(RM) $(OVERLAY).program
	TMPDIR=$(join link_,$(OVERLAY)) $(PARX_OVL_LD) -shared $(WARN_LINK_AS_ERROR) -Wl,-soname,$(OVERLAY)$(PARX_OVL_EXT) $(CPLUSPLUSLDOPTIONS) \
	   @$(OVERLAY).objlist $(PARX_OVL_LIBPATH) $(PARX_OVL_LIBS) $(PARX_OVL_LIBRARIES) \
	  -o $(OVERLAY)$(PARX_OVL_EXT)
	$(RMD) $(join link_,$(OVERLAY))

clean::
	$(RM) $(OVERLAY)$(PARX_OVL_EXT) $(OVERLAY).program

$(foreach obj,$(OBJS),$(eval $(call CREATE_SIMPLE_DEPS,$(obj),.c,$(SRCDIR))))

$(OBJS): $(SRCDIR)/$(OVERLAY)$(PARX_OVL_DEF_EXT) $(OVERLAY)$(OBJEXT)
	$(info Compile $(SRCDIR)/$(@:$(OBJEXT)=.c))
	$(PARCOMP) $(SRCDIR)/$(OVERLAY)$(PARX_OVL_DEF_EXT) $(PARCOMP_FLAGS) -r $(SRCDIR)/${@:$(OBJEXT)=.c} &&\
	$(MV) $(DEPDIR)/$(@F:$(OBJEXT)=.Td) $(DEPDIR)/$(@F:$(OBJEXT)=.d) && touch $@
-include $(addprefix $(DEPDIR)/,$(addsuffix .d,$(basename $(notdir $(OBJS)))))

$(eval $(call CREATE_SIMPLE_DEPS,$(OVERLAY)$(OBJEXT),$(PARX_OVL_DEF_EXT),$(SRCDIR)))
$(OVERLAY)$(OBJEXT):	 | $(DEPDIR)
	$(info Compile $(SRCDIR)/$(OVERLAY)$(PARX_OVL_DEF_EXT))
	$(PARCOMP) $(SRCDIR)/$(OVERLAY)$(PARX_OVL_DEF_EXT)  $(TESTSUITE_FLAGS) $(PARCOMP_FLAGS) &&\
	$(MV) $(DEPDIR)/$(@F:$(OBJEXT)=.Td) $(DEPDIR)/$(@F:$(OBJEXT)=.d) && touch $@
-include $(DEPDIR)/$(OVERLAY).d

ifeq ($(SRCDIR)/$(OVERLAY).xml,$(wildcard $(SRCDIR)/$(OVERLAY).xml))
install:: $(METHODS_DIR)/$(OVERLAY).xml

$(eval $(call MKDIR_FCN,$(METHODS_DIR)))
$(METHODS_DIR)/$(OVERLAY).xml : $(SRCDIR)/$(OVERLAY).xml | $(METHODS_DIR)
	$(info Install $(METHODS_DIR)/$(OVERLAY).xml)
	$(RM) $(METHODS_DIR)/$(OVERLAY).xml
	$(CPASC) $(SRCDIR)/$(OVERLAY).xml $(METHODS_DIR)/$(OVERLAY).xml

instclean: instclean.xml

.PHONY : instclean.xml
instclean.xml:
	$(RM) $(METHODS_DIR)/$(OVERLAY).xml

instlist: instlist.xml

.PHONY : instlist.xml
instlist.xml:
	@echo $(METHODS_DIR)/$(OVERLAY).xml

clean:: instclean
endif

ifeq ($(SRCDIR)/$(OVERLAY).html,$(wildcard $(SRCDIR)/$(OVERLAY).html))
install:: $(METHODS_DIR)/$(OVERLAY).html

$(eval $(call MKDIR_FCN,$(METHODS_DIR)))
$(METHODS_DIR)/$(OVERLAY).html : $(SRCDIR)/$(OVERLAY).html | $(METHODS_DIR)
	$(info Install $(METHODS_DIR)/$(OVERLAY).html)
	$(RM) $(METHODS_DIR)/$(OVERLAY).html
	$(CPASC) $(SRCDIR)/$(OVERLAY).html $(METHODS_DIR)/$(OVERLAY).html

instclean: instclean.html

.PHONY : instclean.html
instclean.html:
	$(RM) $(METHODS_DIR)/$(OVERLAY).html

instlist: instlist.html

.PHONY : instlist.html
instlist.html:
	@echo $(METHODS_DIR)/$(OVERLAY).html

clean:: instclean
endif

$(eval $(call COPY_TARGET,$(OVERLAY)$(PARX_OVL_EXT),$(METHODS_DIR)/$(notdir $(OVERLAY)$(PARX_OVL_EXT))))
install:: $(METHODS_DIR)/$(notdir $(OVERLAY)$(PARX_OVL_EXT))

instclean: instclean$(PARX_OVL_EXT)

.PHONY : instclean$(PARX_OVL_EXT)
instclean$(PARX_OVL_EXT):
	$(RM) $(METHODS_DIR)/$(OVERLAY)$(PARX_OVL_EXT)

instlist: instlist$(PARX_OVL_EXT)

.PHONY : instlist$(PARX_OVL_EXT)
instlist$(PARX_OVL_EXT):
	@echo $(METHODS_DIR)/$(OVERLAY)$(PARX_OVL_EXT)

clean:: instclean

installppg : $(PPG_DIR)/$(notdir $(SRCDIR)/$(OVERLAY).ppg)

$(eval $(call MKDIR_FCN,$(PPG_DIR)))
$(PPG_DIR)/$(notdir $(SRCDIR)/$(OVERLAY).ppg) : forceppg | $(PPG_DIR)
	$(info Install $(PPG_DIR)/$(notdir $(SRCDIR)/$(OVERLAY).ppg))
	$(RM) $(PPG_DIR)/$(notdir $(SRCDIR)/$(OVERLAY).ppg)
	$(CP) $(SRCDIR)/$(OVERLAY).ppg $(PPG_DIR)/$(notdir $(SRCDIR)/$(OVERLAY).ppg)

instclean: instclean$(notdir $(SRCDIR)/$(OVERLAY).ppg)

.PHONY : instclean$(notdir $(SRCDIR)/$(OVERLAY).ppg)
instclean$(notdir $(SRCDIR)/$(OVERLAY).ppg):
	$(RM) $(PPG_DIR)/$(notdir $(SRCDIR)/$(OVERLAY).ppg)

instlist: instlist$(notdir $(SRCDIR)/$(OVERLAY).ppg)

.PHONY : instlist$(notdir $(SRCDIR)/$(OVERLAY).ppg)
instlist$(notdir $(SRCDIR)/$(OVERLAY).ppg):
	@echo $(PPG_DIR)/$(notdir $(SRCDIR)/$(OVERLAY).ppg)

clean:: instclean

showppg ::
	@echo $(notdir $(SRCDIR)/$(OVERLAY).ppg)

cproto::
	-if [ ! -r relProtos_p.h ]; then			  		\
		$(TOUCH) relProtos_p.h;				\
	fi
	$(CAT) < $(PARX_PROTOHEAD) > relProtos.new
	$(CPROTO) $(CPROTOFLAGS) -O relProtos.err $(SRCS) >> relProtos.new
	$(CAT) < $(PARX_PROTOFOOT) >> relProtos.new
	$(CAT) relProtos.err
	file=relProtos.err; test -z "`cat $$file`"
	$(CMP) -s relProtos_p.h relProtos.new || \
	{ \
		$(ECHO) Install prototype file relProtos_p.h; \
		$(RM) relProtos_p.h; \
		$(MV) relProtos.new relProtos_p.h; \
	}
	$(RM) relProtos.new
	$(RM) relProtos.err

emptyrule::

test::

cproto::

clean::
	$(RM_CMD)

depend::

Makefiles::

all::

sca::

install::

dll::

idl::

docu::

cproto::

