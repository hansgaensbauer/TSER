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

#define DEBUG	    1
#define DB_MODULE   1
#define DB_LINE_NR  1


#include "method.h"

void initMeth()
{
  DB_MSG(( "--> initMeth" ));


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

  /* init encoding parameters                                   */
  STB_InitEncoding();

  if(ParxRelsParHasValue("NEchoes") == No)
    NEchoes = 1024;

  if(ParxRelsParHasValue("PVM_EchoTime") == No)
    PVM_EchoTime = 1;

  if(ParxRelsParHasValue("PVM_Fov") == No)
    PVM_Fov[0] = 108;

  if(ParxRelsParHasValue("PVM_SliceThick") == No)
    PVM_SliceThick = 5;

  if(ParxRelsParHasValue("NPts") == No)
    NPts = 16;

  //Set the correct default for well plates

  ACQ_GradientMatrix[0][0][0] = 0.0;
  ACQ_GradientMatrix[0][0][1] = 0.0;
  ACQ_GradientMatrix[0][0][2] = 1.0;
  ACQ_GradientMatrix[0][1][0] = 0.0;
  ACQ_GradientMatrix[0][1][1] = 1.0;
  ACQ_GradientMatrix[0][1][2] = 0.0;
  ACQ_GradientMatrix[0][2][0] = 1.0;
  ACQ_GradientMatrix[0][2][1] = 0.0;
  ACQ_GradientMatrix[0][2][2] = 0.0;

  /* init geometry parameters                                   */
  //STB_InitImageGeometry();

  /* initialize standard imaging parameters NA TR TE DS         */
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


