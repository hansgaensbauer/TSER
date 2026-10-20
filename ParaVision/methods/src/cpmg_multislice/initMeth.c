/* ***************************************************************
 *
 * $Source$
 *
 * Copyright (c) 2007
 * Bruker BioSpin MRI GmbH
 * D-76275 Ettlingen, Germany
 *
 * All Rights Reserved
 *
 *
 * $Id$
 *
 * ***************************************************************/

static const char resid[] = "$Id$ (c) 2007 Bruker BioSpin MRI GmbH";

#define DEBUG	    0
#define DB_MODULE   0
#define DB_LINE_NR  0


#include "method.h"

void initMeth()
{
  DB_MSG(( "--> initMeth" ));

  int dimRange[2]   = { 1, 1 };
  int lowMat[3]     = { 2, 2, 2 };
  int upMat[3]      = { 64, 256, 256 };
  int defaultMat[3] = { 12, 128, 64 };

  /* initialization of PVM_Nucleus1                             */
  STB_InitNuclei(1);

  /* Initialisation of rf pulse parameters */

  STB_InitRFPulse("ExcPulse1",      // name of pulse structure
                  "ExcPulse1Enum",  // name of pulse list parameter
                  "ExcPulse1Ampl",  // name of pulse amplitude parameter
                  "ExcPulse1Shape", // name of pulse shape (for calc. pulses)
                  0,                // used for excitation
                  "Calculated",     // default shape
                  2000.0,           // default bandwidth
                  90.0);            // default pulse angle

  // check valid range for this specific pulse see parsRelations.c
  ExcPulse1Range();

  STB_InitRFPulse("RefPulse1",      // name of pulse structure
                  "RefPulse1Enum",  // name of pulse list parameter
                  "RefPulse1Ampl",  // name of pulse amplitude parameter
                  "RefPulse1Shape", // name of pulse shape (for calc. pulses)
                  1,                // used for refocusing
                  "Calculated",     // default shape
                  2000.0,           // default bandwidth
                  180.0);           // default pulse angle

  RefPulse1Range();

  if(ParxRelsParHasValue("NEchoes") == No)
    NEchoes = 1024;

  if(ParxRelsParHasValue("PVM_EchoTime") == No)
    PVM_EchoTime = 2;

  if(ParxRelsParHasValue("PVM_Fov") == No)
    PVM_Fov[0] = 50;

  if(ParxRelsParHasValue("PVM_SliceThick") == No)
    PVM_SliceThick = 5;

  if(ParxRelsParHasValue("NPts") == No)
    NPts = 32;

  if(ParxRelsParHasValue("RecoveryTime") == No)
    RecoveryTime = 5000;


  /* init encoding parameters                                   */
  STB_InitEncoding( 1, dimRange, lowMat, upMat, defaultMat);

  /* init geometry parameters                                   */
  STB_InitImageGeometry();

  /* initialize standard imaging parameters NA TR TE DS         */
  RepetitionTimeRange();
  EchoTimeRange();
  if(ParxRelsParHasValue("NDummyScans") == No)
    NDummyScans = 0;
  if(ParxRelsParHasValue("PVM_DeriveGains") == No)
    PVM_DeriveGains = Yes;
 
  /* Visibility of parameters                                   */
  ParxRelsMakeNonEditable("PVM_EchoPosition,"
                          "PVM_AcquisitionTime,"
                          "PVM_MinEchoTime");
 
  /* Once all parameters have initial values, the backbone is 
   * called to assure they are consistent                       */
  
  backbone();
 
  DB_MSG(( "<-- initMeth" ));
}

/****************************************************************/
/*		E N D   O F   F I L E				*/
/****************************************************************/


