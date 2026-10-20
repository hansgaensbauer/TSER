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

static const char resid[] = "$Id$ (C) 2007 Bruker BioSpin MRI GmbH";

#define DEBUG		1
#define DB_MODULE	1
#define DB_LINE_NR	1


#include "method.h"

void SetRecoParam( void )

{ 
  DB_MSG(("-->SetRecoParam"));

  /* set baselevel reconstruction parameters */
  
  ATB_InitUserModeReco(
    1,
    0,
    PVM_EncMatrix,
    PVM_Matrix,
    NULL,
    NULL,
    NI,
    ACQ_obj_order,
    1,
    NULL,
    NULL,
    NULL,
    PVM_EncNReceivers,
    PVM_EncChanScaling,
    0,
    1);

  ATB_SetRecoPhaseCorr(PVM_EchoPosition, 0.0, 0);
  DB_MSG(("<--SetRecoParam"));  
}

void DeriveReco(void)
{
  DB_MSG(("-->DeriveReco"));

  if (RecoUserUpdate == No)
  {
    DB_MSG(("<--RecoDerive: no update"));
    return;
  }

  ParxRelsParRelations("RecoUserUpdate", Yes);

  //Filter for ArrayPhase Adjustment
  ATB_GetRecoDataPoints(PVM_RecoDataPointsRequired,  PVM_EncNReceivers*RECO_inp_size[0]*2, "Q");
  
  DB_MSG(("<--DeriveReco"));
 
}


