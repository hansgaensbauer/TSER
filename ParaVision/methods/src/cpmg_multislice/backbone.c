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

#define DEBUG		0
#define DB_MODULE	0
#define DB_LINE_NR	0

#include "method.h"

void backbone(void)
{
  double ReadGradDur;
  double minFov[1];
  double minSliceThick;
  // double dval;
  // int dim;

  DB_MSG(("-->backbone"));

  /* update nuclei parameter group                            */

  STB_UpdateNuclei(No);

  /* update parameters controlling the data sampling period   */

  // MRT_UpdateDigPars(&PVM_EffSWh,
  //                    PVM_EncMatrix[0],
  //                   &PVM_AntiAlias[0],
  //                   &PVM_AcquisitionTime);

  double riseTime = CFG_GradientRampTime();
  ReadGradDur = PVM_EchoTime - RefPulse1.Length - 0.02; //Includes ramps
  PVM_AcquisitionTime = ReadGradDur - riseTime * 2;

  PVM_EffSWh = NPts/PVM_AcquisitionTime * 1000.0;

  PVM_EncMatrix[0] = NPts;
  PVM_Matrix[0] = NPts;

  /* update pulses                                  */  
  
  STB_UpdateRFPulse("ExcPulse1",1,PVM_DeriveGains,Conventional);
  STB_UpdateRFPulse("RefPulse1",1,PVM_DeriveGains,Conventional);

  PVM_NRepetitions = 1;

  /* calculate limits for read phase and slice                */
  
  ReadDephGradLim       = 
    ReadGradLim         =
    ExcSliceRephGradLim =
    ExcSliceGradLim     = 50.0;

   
  /* calculate gradients in logical directions                */
  double effEncGradDur = ReadGradDur - riseTime;
  double RephGradDur = (PVM_EchoTime - RefPulse1.Length - ExcPulse1.Length - 0.02)/2 - riseTime;
  double effRephGradDur = RephGradDur - riseTime;

  double readDephGradRatio = 0.5*effEncGradDur/effRephGradDur;

  double effSliceGradDur = (ExcPulse1.Length + riseTime) * ExcPulse1.Rpfac/100;
  
  double sliceGradRatio = effSliceGradDur/effRephGradDur;

  /* calculate minima for FOV and slice thickness             */

  minFov[0] = MRT_MinReadFov(PVM_EffSWh,
                             readDephGradRatio,
                             ReadGradLim,
                             ReadDephGradLim,
                             PVM_GradCalConst);
  
  minSliceThick = MRT_MinSliceThickness(ExcPulse1.Bandwidth,
                                         sliceGradRatio,
                                         ExcSliceGradLim,
                                         ExcSliceRephGradLim,
                                         PVM_GradCalConst);


  STB_UpdateImageGeometry(1, 
                          PVM_Matrix,
                          minFov,
                          0, /* total slices (no restr) */
                          0, /* total slice packages (no restr) */
                          0,
                          minSliceThick,
                          1.0); /* sliceFovRatio in 3D */


  /* calculate gradients in logical directions                */
  UpdateGradients(readDephGradRatio,sliceGradRatio);

  STB_UpdateEncoding(
    NULL,               /* pointer to required segment size */
    SEG_SEQUENTIAL,     /* segmenting mode      */
    Yes,                /* allow PI in 2nd dim  */ 
    Yes,                /* allow PI ref lines in 2nd dim  */
    Yes,                /* partial ft in 2nd dim */
    &PVM_EchoPosition); /* partial ft in 1nd dim */

  /* calculate frequency offsets                              */
  UpdateFrequencyOffsets();

  /*  update sequence timing                                  */
  UpdateRepetitionTime();

  PVM_NEchoImages = NEchoes;

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
  
  int nslices = GTB_NumberOfSlices( PVM_NSPacks, PVM_SPackArrNSlices );

  double riseTime = CFG_GradientRampTime();
  PVM_RepetitionTime =
  nslices * (
    riseTime +
    ExcPulse1.Length +
    PVM_EchoTime-RefPulse1.Length-riseTime + //D3
    riseTime +
    PVM_EchoTime/2.0 + 
    NEchoes * PVM_EchoTime + RecoveryTime);

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

  nslices = GTB_NumberOfSlices(PVM_NSPacks,PVM_SPackArrNSlices);

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





