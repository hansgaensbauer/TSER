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

/* ************************************************************
 * redirection of global parameter groups 
 * ***********************************************************/

/* react on changes of system configuration */
relations PVM_SysConfigHandler        backbone;

/* geometry */
relations PVM_ImageGeometryHandler    backbone;

/* nuclei */
relations PVM_NucleiHandler           backbone; 

/* encoding parameter group */
relations PVM_EncodingHandler         backbone;

/* ************************************************************
 * relation redirection of single global parameters used in
 * this method:
 * ***********************************************************/

relations PVM_RepetitionTime          RepetitionTimeRel;

relations PVM_EchoTime                EchoTimeRel;
relations PVM_MinEchoTime             backbone;

relations PVM_AcquisitionTime         backbone;
relations PVM_DeriveGains             backbone;
relations PVM_EffSWh                  backbone;

/* ************************************************************
 * parameters that are used but not shown in editor
 * only the method may change these parameters, they
 * are redirected to the backbone routine.
 * ************************************************************/

relations PVM_NRepetitions            backbone;     
relations PVM_MinRepetitionTime       backbone;
relations PVM_NEchoImages             backbone;

/* react on parameter adjustments */
relations PVM_AdjResultHandler        backbone;
