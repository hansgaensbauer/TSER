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
 * $Id$
 *
 * ***************************************************************/

/****************************************************************/
/* INCLUDE FILES						*/
/****************************************************************/

/* =============================================================
 * Definition of local method parameters. Parameters that are
 * not editable and calculated inside the methods backbone such
 * as gradient values will have the backbone routine as default
 * relations. Only parameters that appear editable in the method
 * editor need a specific parameter relation and range checking
 * function.
 * ============================================================*/

/* -------------------------------------------------------
 * Frequency encoding parameter 
 * ------------------------------------------------------*/

double parameter
{
  display_name "Read Dephase Gradient";
  format "%f";
  units  "%";
  editable false;
  relations backbone;
}ReadDephGrad;

double parameter
{
  display_name "Read Gradient";
  format "%f";
  units "%";
  editable false;
  relations backbone;
}ReadGrad;

/* ----------------------------------------------------------
 * Read spoiler parameter
 * ---------------------------------------------------------*/


/* ---------------------------------------------------------------
 * Slice selection parameter
 * --------------------------------------------------------------*/

double parameter
{
  display_name "Exc. Slice Gradient";
  format "%f";
  units  "%";
  editable false;
  relations backbone;
}ExcSliceGrad;

double parameter
{
  display_name "Exc. Slice Reph. Gradient";
  format "%f";
  units  "%";
  editable false;
  relations backbone;
}ExcSliceRephGrad;


/* ----------------------------------------------------------
 * Definition of RF Pulse parameter
 * ---------------------------------------------------------*/

PV_PULSE_LIST parameter
{
  display_name "Excitation Pulse Shape";
  relations    ExcPulse1EnumRelation;
}ExcPulse1Enum;


PVM_RF_PULSE parameter
{
  display_name "Excitation Pulse";
  relations    ExcPulse1Relation;
}ExcPulse1;

PVM_RF_PULSE_AMP_TYPE parameter
{
  display_name "Exc Pulse Amplitude";
  relations ExcPulse1AmplRel;
}ExcPulse1Ampl;

double parameter
{
  relations backbone;
}ExcPulse1Shape[];



PV_PULSE_LIST parameter
{
  display_name "Refocusing Pulse Shape";
  relations    RefPulse1EnumRelation;
}RefPulse1Enum;


PVM_RF_PULSE parameter
{
  display_name "Refocusing Pulse";
  relations    RefPulse1Relation;
}RefPulse1;

PVM_RF_PULSE_AMP_TYPE parameter
{
  display_name "Rfc Pulse Amplitude";
  relations RefPulse1AmplRel;
}RefPulse1Ampl;

double parameter
{
  relations backbone;
}RefPulse1Shape[];


/* ---------------------------------------------------------
 * remaining local method parameters
 * --------------------------------------------------------*/

int parameter
{
  display_name "Echoes";
  minimum 1 outofrange nearestval;
  maximum 4096 outofrange nearestval;
  relations backbone;
} NEchoes;

int parameter
{
  display_name "Points";
  minimum 1 outofrange nearestval;
  maximum 32 outofrange nearestval;
  relations backbone;
} NPts;

int parameter 
{
  display_name "Dummy Scans";
  relations backbone;
  minimum 0 outofrange nearestval;
} NDummyScans;


/* ---------------------------------------------------------
 * auxiliary method parameters
 * --------------------------------------------------------*/
double parameter {editable false;}ReadDephGradLim;
double parameter {editable false;}ReadGradLim;
double parameter {editable false;}Phase2DGradLim;
double parameter {editable false;}Phase3DGradLim;
double parameter {editable false;}ExcSliceGradLim;
double parameter {editable false;}ExcSliceRephGradLim;

/****************************************************************/
/*	E N D   O F   F I L E					*/
/****************************************************************/


