/****************************************************************
 *
 * $Source$
 *
 * Copyright (c) 2014
 * Bruker BioSpin MRI GmbH
 * D-76275 Ettlingen, Germany
 *
 * All Rights Reserved
 *
 * $Id$
 *
 ****************************************************************/

#if defined(__GNUC__)  && __GNUC__ >= 4 && !defined(CPROTO)
#pragma GCC visibility push(hidden)
#endif

/****************************************************************
 *
 * START of definitions automatically created by CPROTO. Do not change.
 *
 ****************************************************************/
/* /common/KI-CPMG/PV/methods/src/cpmg_1d/initMeth.c */
void initMeth(void);
/* /common/KI-CPMG/PV/methods/src/cpmg_1d/loadMeth.c */
void loadMeth(const char *);
/* /common/KI-CPMG/PV/methods/src/cpmg_1d/backbone.c */
void backbone(void);
void UpdateRepetitionTime(void);
void UpdateGradients(double, double);
void UpdateFrequencyOffsets(void);
/* /common/KI-CPMG/PV/methods/src/cpmg_1d/parsRelations.c */
void ExcPulse1EnumRelation(void);
void ExcPulse1AmplRel(void);
void HandleRFPulseAmplitudes(void);
void ExcPulse1Relation(void);
void ExcPulse1Range(void);
void RefPulse1EnumRelation(void);
void RefPulse1AmplRel(void);
void RefPulse1Relation(void);
void RefPulse1Range(void);
/* /common/KI-CPMG/PV/methods/src/cpmg_1d/BaseLevelRelations.c */
void SetBaseLevelParam(void);
void SetBasicParameters(void);
void SetFrequencyParameters(void);
void SetGradientParameters(void);
void SetPpgParameters(void);
void SetAcquisitionParameters(void);
void SetInfoParameters(void);
void PrintTimingInfo(void);
/* /common/KI-CPMG/PV/methods/src/cpmg_1d/RecoRelations.c */
void SetRecoParam(void);
void DeriveReco(void);

/****************************************************************
 *
 * END of definitions created by cproto.
 *
 ****************************************************************/
/****************************************************************
 *
 * $Source$
 *
 * Copyright (c) 2014
 * Bruker BioSpin MRI GmbH
 * D-76275 Ettlingen, Germany
 *
 * All Rights Reserved
 *
 * $Id$
 *
 ****************************************************************/

#if defined(__GNUC__)  && __GNUC__ >= 4 && !defined(CPROTO)
#pragma GCC visibility pop
#endif

