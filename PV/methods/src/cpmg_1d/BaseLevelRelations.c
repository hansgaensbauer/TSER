/* ***************************************************************
 *
 * Copyright (c) 2007-2018
 * Bruker BioSpin MRI GmbH
 * D-76275 Ettlingen, Germany
 *
 * All Rights Reserved
 *
 * $Id$
 *
 * ***************************************************************/

static const char resid[] = "$Id$ (c) 2007-2018 Bruker BioSpin MRI GmbH";


#define DEBUG		 1
#define DB_MODULE	 1
#define DB_LINE_NR	 1




#include "method.h"

void SetBaseLevelParam()
{
  DB_MSG(("-->SetBaseLevelParam"));

  SetBasicParameters();
  
  SetFrequencyParameters();
  
  SetPpgParameters();

  SetAcquisitionParameters();
  
  SetGradientParameters();
  
  SetInfoParameters();
  
  ATB_SetReceiverGains();

#if DEBUG
  PrintTimingInfo();
#endif

  DB_MSG(("<--SetBaseLevelParam")); 
}

void SetBasicParameters( void )
{
  DB_MSG(("-->SetBasicParameters"));
      
  /* NSLICES */  
  ATB_SetNSlices(1);

  /* NR */  
  ATB_SetNR( PVM_NRepetitions );

  /* NI */  
  ATB_SetNI(NEchoes);
  
  /* AVERAGING */
  ATB_SetNA( 1 );
  ATB_SetNAE( 1 );
  // switch(PVM_MotionSupOnOff)
  // {
  //   default:
  //   case Off:
  //     ATB_SetNA( PVM_NAverages );
  //     ATB_SetNAE( 1 );
  //     break;
  //   case On:
  //     ATB_SetNAE( PVM_NAverages );
  //     ATB_SetNA( 1 );
  //     break;
  // }
 
  /* NECHOES */ 
  NECHOES = NEchoes;
   
  /* ACQ_obj_order */
  PARX_change_dims("ACQ_obj_order",NI);
  
  DB_MSG(("<--SetBasicParameters"));
}

void SetFrequencyParameters( void )
{
  DB_MSG(("-->SetFrequencyParameters"));

  ATB_SetNuc1(PVM_Nucleus1);
   
  sprintf(NUC2,"off");
  sprintf(NUC3,"off");
  sprintf(NUC4,"off");
  sprintf(NUC5,"off");
  sprintf(NUC6,"off");
  sprintf(NUC7,"off");
  sprintf(NUC8,"off");
  
  ATB_SetNucleus(PVM_Nucleus1);

  ACQ_O1_mode = BF_plus_Offset_list;
  ParxRelsParRelations("ACQ_O1_mode",Yes);
  
  O1 = 0.0;
  O2 = 0.0;
  O3 = 0.0;
  O4 = 0.0;
  O5 = 0.0;
  O6 = 0.0;
  O7 = 0.0;
  O8 = 0.0;
  
  /* Set BF's to working freuncies on used channels */
  ACQ_BF_enable = No;
  BF1 = PVM_FrqWork[0];
  BF2 = PVM_FrqWork[1];
  /* call relations of BF1 (no need for other BF's) */
  ParxRelsParRelations("BF1", Yes); 

  int nslices = 1;
 
  
  ATB_SetAcqO1List( nslices,
                    PVM_ObjOrderList,
                    PVM_SliceOffsetHz );
 
  
  ATB_SetAcqO1BList( nslices,
                     PVM_ObjOrderList,
                     PVM_ReadOffsetHz);
 
  DB_MSG(("<--SetFrequencyParameters"));
}


void SetGradientParameters( void )
{
  DB_MSG(("-->SetGradientParameters"));
   
  // int spatDim = PTB_GetSpatDim();
  // PARX_change_dims("ACQ_phase_encoding_mode", spatDim );
  // PARX_change_dims("ACQ_phase_enc_start", spatDim );

  // switch(spatDim)
  //   {
  //   case 3:
  //     ACQ_phase_encoding_mode[2] = User_Defined_Encoding;
  //     ACQ_phase_enc_start[2]     = -1; /* set but not used     */
  //     ACQ_spatial_size_2 = PVM_EncMatrix[2];
  //     ParxRelsCopyPar("ACQ_spatial_phase_2","PVM_EncValues2");
  //     /* no break, falls through                               */
  //   case 2:
  //     ACQ_phase_encoding_mode[1] = User_Defined_Encoding;
  //     ACQ_phase_enc_start[1]     = -1; /* set but not used     */
  //     ACQ_spatial_size_1 = PVM_EncMatrix[1];
  //     ParxRelsCopyPar("ACQ_spatial_phase_1","PVM_EncValues1");
  //     /* no break, falls through                               */
  //   case 1:
  //   default:
  //     ACQ_phase_encoding_mode[0] = Read;
  //     ACQ_phase_enc_start[0]     = -1;
  //     break;
  // }

  ACQ_scaling_read  = 1.0;
  // ACQ_scaling_phase = 1.0;
  ACQ_scaling_slice = 1.0;
  
  /* gradient amplitudes */
  ACQ_gradient_amplitude[0] =  ExcSliceGrad;
  ACQ_gradient_amplitude[1] = -ExcSliceRephGrad;
  ACQ_gradient_amplitude[2] =  ReadDephGrad;
  ACQ_gradient_amplitude[5] =  ReadGrad;
  
  DB_MSG(("<--SetGradientParameters"));
}

void SetPpgParameters(void)
{

  DB_MSG(("-->SetPpgParameters"));
  double riseTime;
  riseTime = CFG_GradientRampTime();
  ATB_SetPulprog("cpmg_1d.ppg");

  // L[0] = PVM_EncMatrix[1];

  // L[1] = 1;

  L[2] = NDummyScans;

  D[0]  = ((PVM_RepetitionTime - PVM_MinRepetitionTime) 
            + 0.01)/1000.0;
  D[2]  = PVM_AcquisitionTime/1000.0;
  D[1]  = riseTime/1000.0;
  D[3]  = (PVM_EchoTime - RefPulse1.Length - riseTime - 0.02) / 1000.0;
  D[4]  = ((PVM_EchoTime - RefPulse1.Length)/2 + riseTime - 0.01)/1000.0;
  
  /* set shaped pulses:
     in this method ACQ_RfShapes[0] is used           
     the pulse duration is stored in baselevel parameter P[0]
  */
  ATB_SetRFPulse("ExcPulse1","ACQ_RfShapes[0]","P[0]");
  ATB_SetRFPulse("RefPulse1","ACQ_RfShapes[1]","P[1]");
  
  DB_MSG(("<--SetPpgParameters"));
}

void SetAcquisitionParameters(void)
{  
  DB_MSG(("-->SetAcquisitionParameters"));
  
  /* Job 0 */
  JOBPARAMETERS(jobParameters);
  JOBDESCRIPTION job0=jobParameters->getOrCreateJob("job0");

  job0->initPars(1, NPts, PVM_EffSWh);
  job0->appendLoop(NI);
  job0->appendLoop(NDummyScans, LOOP_DUMMIES);

  DB_MSG(("<--SetAcquisitionParameters"));  
}


void SetInfoParameters( void )
{
  int slices, i, spatDim;
  
  DB_MSG(("-->SetInfoParameters"));
  
  spatDim = 1;
 
  /* ACQ_dim */
  ACQ_dim = spatDim;
  ParxRelsParRelations("ACQ_dim",Yes);
  
  /* ACQ_dim_desc */
  ATB_SetAcqDimDesc( 0, spatDim, NULL ); 
  ATB_SetAcqFov( Spatial, spatDim, PVM_Fov, PVM_AntiAlias );
  
  ACQ_flip_angle = ExcPulse1.Flipangle;
  
  PARX_change_dims("ACQ_echo_time",1);

  ACQ_echo_time[0] = PVM_EchoTime;
  
  PARX_change_dims("ACQ_inter_echo_time",1);
  ACQ_inter_echo_time[0] = PVM_EchoTime;
  
  PARX_change_dims("ACQ_repetition_time",1);
  ACQ_repetition_time[0] = PVM_RepetitionTime;
  
  PARX_change_dims("ACQ_recov_time",1);
  ACQ_recov_time[0] =  
    PVM_RepetitionTime - 
    (PVM_EchoTime/2 + ExcPulse1.Length/2);
  
  PARX_change_dims("ACQ_inversion_time",1);
  ACQ_inversion_time[0] = PVM_InversionTime;
  
  //ATB_SetAcqSliceAngle( PtrType3x3 PVM_SPackArrGradOrient[0],
	//		PVM_NSPacks );
  
  ACQ_slice_orient = Arbitrary_Oblique;
  
  ACQ_slice_thick = PVM_SliceThick;
  
  slices = 1;
  
  PARX_change_dims("ACQ_slice_offset",slices);
  PARX_change_dims("ACQ_read_offset",slices);
  PARX_change_dims("ACQ_phase1_offset",slices);
  PARX_change_dims("ACQ_phase2_offset",slices);
  
  for(i=0;i<slices;i++)
  {
    ACQ_slice_offset[i]  = PVM_SliceOffset[i];
    ACQ_read_offset[i]   = PVM_ReadOffset[i];
    ACQ_phase1_offset[i] = PVM_Phase1Offset[i];
    ACQ_phase2_offset[i] = PVM_Phase2Offset[i];
  }
  
  ACQ_read_ext = (int)PVM_AntiAlias[0];
  
  PARX_change_dims("ACQ_slice_sepn", slices==1 ? 1 : slices-1);
  
  if( slices == 1 )
  {
    ACQ_slice_sepn[0] = 0.0;
  }
  else
  {
    for( i=1; i<slices;i++ )
    {
      ACQ_slice_sepn[i-1]=PVM_SliceOffset[i]-PVM_SliceOffset[i-1];
    }
  }
  
 // ATB_SetAcqSliceSepn( PVM_SPackArrSliceDistance,
  //                     PVM_NSPacks );
  
   
  ACQ_n_t1_points = 1;
    
  if( ParxRelsParHasValue("ACQ_contrast_agent") == No )
  {
    ACQ_contrast_agent[0] = '\0';
  }
  
  if( ParxRelsParHasValue("ACQ_contrast") == No )
  {
    ACQ_contrast.volume = 0.0;
    ACQ_contrast.dose = 0.0;
    ACQ_contrast.route[0] = '\0';
    ACQ_contrast.start_time[0] = '\0';
    ACQ_contrast.stop_time[0] = '\0';
  }
  
  ParxRelsParRelations("ACQ_contrast_agent",Yes);
  
  ACQ_position_X = 0.0;
  ACQ_position_Y = 0.0;
  ACQ_position_Z = 0.0;

  PARX_change_dims("ACQ_temporal_delay",1);
  ACQ_temporal_delay[0] = 0.0;
  
  ACQ_RF_power = 0;
  
  // initialize ACQ_n_echo_images ACQ_echo_descr
  //            ACQ_n_movie_frames ACQ_movie_descr
  ATB_ResetEchoDescr();
  ATB_ResetMovieDescr();
  
  
  DB_MSG(("<--SetInfoParameters"));  
}


#if DEBUG

void PrintTimingInfo(void)
{

/*
  double te,tr;

  DB_MSG(("-->PrintTimingInfo"));

  te=(P[0])/2000.0+(D[3]+D[5]+D[4])*1000.0 +
      PVM_AcquisitionTime*PVM_EchoPosition/100.0;

  tr = (te+P[0]/2000.0 + 0.01 + 
	(D[0]+D[1]+D[3]+D[6]+D[7])*1000
	+ PVM_AcquisitionTime*(100.0-PVM_EchoPosition)/100.0)*NSLICES;
  
  DB_MSG(("TE : %f should be: %f diff %f\n",
	  te,PVM_EchoTime,
	  te-PVM_EchoTime));

  DB_MSG(("tr: %f  should be: %f  diff %f\n",
          tr,PVM_RepetitionTime,
	  tr-PVM_RepetitionTime));

  DB_MSG(("<--PrintTimingInfo"));  

*/
}
#endif
