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


static const char resid[] = "$Id $ (c) 2007 Bruker BioSpin MRI GmbH";

#define DEBUG		1
#define DB_MODULE	1
#define DB_LINE_NR	1

#include "method.h"

void backbone(void)
{
  double ReadGradDur;

  DB_MSG(("-->backbone"));

  /* update nuclei parameter group                            */

  STB_UpdateNuclei(No);


  /* update parameters controlling the data sampling period   */
  
  // MRT_UpdateDigPars(&EffSWh,
  //                   NPts,
  //                   NULL,
  //                   &PVM_AcquisitionTime);
  double riseTime = CFG_GradientRampTime();
  ReadGradDur = PVM_EchoTime - RefPulse1.Length - 0.02; //Includes ramps
  PVM_AcquisitionTime = ReadGradDur - riseTime * 2;

  PVM_EffSWh = NPts/PVM_AcquisitionTime * 1000.0;

  PVM_EncMatrix[0] = NPts;
  PVM_Matrix[0] = NPts;
  /* update excitation pulse                                  */  
  
  STB_UpdateRFPulse("ExcPulse1",1,PVM_DeriveGains,Conventional);
  STB_UpdateRFPulse("RefPulse1",1,PVM_DeriveGains,Conventional);
  
  
  /*  final handling of PVM_NRepetitions by range checker
   *  to be implemented as exercise, consider the
   *  relation redirection in callbackDefs.h                  */

  PVM_NRepetitions = 1;

  /* calculate limits for read phase and slice                */
  
  ReadDephGradLim       = 
    ReadGradLim         =
    ExcSliceRephGradLim =
    ExcSliceGradLim     = 50.0;


  /* calculate gradients in logical directions                */
  double effEncGradDur = ReadGradDur - riseTime;
  double readDephGradRatio = 0.5;

  double effSliceGradDur = (ExcPulse1.Length + riseTime) * ExcPulse1.Rpfac/100;
  
  double sliceGradRatio = effSliceGradDur/effEncGradDur;

  UpdateGradients(readDephGradRatio,sliceGradRatio);

  STB_UpdateEncoding();

  /* calculate frequency offsets                              */
  UpdateFrequencyOffsets();

  /*  update sequence timing                                  */
  UpdateRepetitionTime();

  PVM_NEchoImages = 1;

  SetBaseLevelParam();
  SetRecoParam();
  
  DB_MSG(("<--backbone"));

}

/*-------------------------------------------------------
 * local utility routines to simplify the backbone 
 *------------------------------------------------------*/

void UpdateRepetitionTime(void)
{

  DB_MSG(("-->UpdateRepetitionTime"));
  
  double riseTime = CFG_GradientRampTime();
  PVM_RepetitionTime =
    riseTime +
    ExcPulse1.Length +
    PVM_EchoTime-RefPulse1.Length-riseTime + //D3
    riseTime +
    PVM_EchoTime/2.0 + 
    NEchoes * PVM_EchoTime;


  PVM_ScanTime = PVM_RepetitionTime;
  UT_ScanTimeStr(PVM_ScanTimeStr,PVM_RepetitionTime);
  ParxRelsShowInEditor("PVM_ScanTimeStr");
  ParxRelsMakeNonEditable("PVM_ScanTimeStr");

  DB_MSG(("<--UpdateRepetitionTime"));
}

void UpdateGradients(double readGradRatio,
                     double sliceGradRatio)
{
  DB_MSG(("-->UpdateGradients"));

  /* Calculation of read phase and slice gradients */


  ReadGrad = MRT_ReadGrad(PVM_EffSWh,
                          PVM_Fov[0],
                          PVM_GradCalConst);

  ReadDephGrad = readGradRatio*ReadGrad;

  ExcSliceGrad = MRT_SliceGrad(ExcPulse1.Bandwidth,
                               PVM_SliceThick,
                               PVM_GradCalConst);

  ExcSliceRephGrad = sliceGradRatio * ExcSliceGrad;

  DB_MSG(("<--UpdateGradients"));
}

void UpdateFrequencyOffsets( void )
{
  int nslices;

  DB_MSG(("-->UpdateFrequencyOffsets"));

  nslices = 1;

  MRT_FrequencyOffsetList(nslices,
                          PVM_EffReadOffset,
                          ReadGrad,
                          PVM_GradCalConst,
                          PVM_ReadOffsetHz );

  MRT_FrequencyOffsetList(nslices,
                          PVM_EffSliceOffset,
                          ExcSliceGrad,
                          PVM_GradCalConst,
                          PVM_SliceOffsetHz );

  DB_MSG(("<--UpdateFrequencyOffsets"));
}





