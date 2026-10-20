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

/* ***************************************************************/
/*	PARAMETER CLASS	               			       	 */
/* ***************************************************************/

/*--------------------------------------------------------------*
 * Definition of the PV class...
 *--------------------------------------------------------------*/

pargroup
{
  ExcPulse1Enum;
  ExcPulse1;
  ExcPulse1Ampl;
  RefPulse1Enum;
  RefPulse1;
  RefPulse1Ampl;
} 
attributes
{
  display_name "RF Pulses";
} RF_Pulses;

pargroup
{
  NDummyScans;
  PVM_AcquisitionTime;
  PVM_EchoPosition;
  ReadGrad;
  ReadDephGrad;
  ExcSliceGrad;		 	 
  ExcSliceRephGrad; 
}SequenceDetails;

extend pargroup
{
  PVM_EchoTime;
  NEchoes;
  PVM_SliceThick;
  PVM_Fov;
  NPts;
  PVM_NEchoImages;
  PVM_ScanTimeStr;
  PVM_ScanTime;
  PVM_DeriveGains;
  RF_Pulses;
  Nuclei;
  Encoding;
  SequenceDetails;
} MethodClass;


/* ***************************************************************/
/*	E N D   O F   F I L E					 */
/* ***************************************************************/

