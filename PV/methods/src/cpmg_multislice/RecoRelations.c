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

#define DEBUG		0
#define DB_MODULE	0
#define DB_LINE_NR	0


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

  DB_MSG(("<--SetRecoParam"));  
}

