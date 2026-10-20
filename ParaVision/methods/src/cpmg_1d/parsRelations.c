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

#define DEBUG		1
#define DB_MODULE	1
#define DB_LINE_NR	1



#include "method.h"

/* =============================================================
 * Default relations and range checking functions of parameters
 * that appear editable in the method editor
 * ============================================================= */

/* ============================================================
 * Globally defined parameters: The relation has been redirected 
 * (see callbackDefs.h)
 * ============================================================ */

/* =============================================================
 * Locally (i.e. in parsDefinition.h) defined parameters
 * ============================================================= */

/*===============================================================
 * ExcPulse1EnumRelation
 * Relation of ExcPulse1Enum (a dynamic enmueration parameter which
 * allows to select one of the existing  pulses)
 *===============================================================*/

void ExcPulse1EnumRelation(void)
{
  DB_MSG(("-->ExcPulse1EnumRelation"));

  UT_SetRequest("ExcPulse1Enum");
  backbone();
  
  DB_MSG(("<--ExcPulse1EnumRelation"));                                       
}

/*===============================================================
 * ExcPulse1AmplRel
 * Relation of ExcPulseAmpl 
 * This parameter is used in the setup parameter card to adjust
 * the RF pulse amplitude manually
 *===============================================================*/

void ExcPulse1AmplRel(void)
{
  DB_MSG(("-->ExcPulse1AmplRel"));
  UT_SetRequest("ExcPulse1Ampl");
  HandleRFPulseAmplitudes();
  DB_MSG(("-->ExcPulse1AmplRel"));
}

void HandleRFPulseAmplitudes(void)
{
  DB_MSG(("-->HandleRFPulseAmplitude"));

  STB_UpdateRFShapeAmplitude("ExcPulse1Ampl,RefPulse1Ampl",No);
  ATB_SetRFPulse("ExcPulse1","ACQ_RfShapes[0]");
  ATB_SetRFPulse("RefPulse1","ACQ_RfShapes[1]");

  DB_MSG(("<--HandleRFPulseAmplitude"));
}


/* ===================================================================
 * Relation of ExcPulse
 * 
 * All pulses of type PVM_RF_PULSE must have relations like this.
 * However, if you clone this funtion for a different pulse parameter
 * remember to replace the param name in the call to UT_SetRequest!
 *
 * IMPORTANT: this function should not be invoked in the backbone!
 ====================================================================*/

void ExcPulse1Relation(void)
{
  DB_MSG(("-->ExcPulse1Relation\n"));
  
  /*
   * Tell the request handling system that the parameter
   * ExcPulse has been edited 
   */
  
  UT_SetRequest("ExcPulse1");
  
  /* Check the values of ExcPulse */
  
  ExcPulse1Range();
  
  /* 
   * call the backbone; further handling will take place there
   * (by means of STB_UpdateRFPulse)  
   */
  
  backbone();
  
  DB_MSG(("<--ExcPulseRelation\n"));
}



void ExcPulse1Range(void)
{
  DB_MSG(("-->ExcPulse1Range"));
  
  // fields to be controlled may be
  // .Length  
  // .Bandwidth
  // .Flipangle
  // .Calculated
  // .Sharpness
  // .Flatness   
 double dval=ExcPulse1.Flipangle;
  
 ExcPulse1.Flipangle = MIN_OF(180.0,MAX_OF(dval,1.0));

 DB_MSG(("<--ExcPulseRange")); 
}




/* --------------------------------------------------------------
   Relation of RefPulseEnum
   --------------------------------------------------------------*/

void RefPulse1EnumRelation(void)
{
  DB_MSG(("-->RefPulse1EnumRelation"));

  UT_SetRequest("RefPulse1Enum");
  backbone();
  
  DB_MSG(("<--RefPulse1EnumRelation"));                                       
}

/* --------------------------------------------------------------
   Relation of RefPulse1Ampl
   --------------------------------------------------------------*/

void RefPulse1AmplRel(void)
{
  DB_MSG(("-->RefPulse1AmplRel"));
  UT_SetRequest("RefPulse1Ampl");
  HandleRFPulseAmplitudes();
  DB_MSG(("-->RefPulse1AmplRel"));
}


/* -----------------------------------------------------------
   Relation of RefPulse 
   -----------------------------------------------------------*/
void RefPulse1Relation(void)
{
  DB_MSG(("-->RefPulse1Relation\n"));
  
  /* 
   *  Tell the request handling system that the parameter
   *  RefPulse has been edited 
   */

  UT_SetRequest("RefPulse1");

  /* Check the values of RefPulse1 */
  RefPulse1Range();
  
  /* 
   * call the backbone; further handling will take place 
   * there (by means of STB_UpdateRFPulse)  
   */
  
  backbone();

  DB_MSG(("<--RefPulseRelation\n"));
}

void RefPulse1Range(void)
{
  DB_MSG(("-->RefPulse1Range"));
  
  double dval=RefPulse1.Flipangle;
  
  RefPulse1.Flipangle = MIN_OF(270,MAX_OF(dval,1));
    
  DB_MSG(("<--RefPulse1Range\n"));  
}
