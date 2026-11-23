
## DEV (22 Nov 2026, 21:55 CT): C_union3_camspec crashed at start
Cause: Cobaya CamSpec NPIPE cache-file lock (CamSpec_NPIPE_12_6_cl_covinv_*.npy.locked) held by a sibling process launched at the same moment. No likelihood value was computed. Per D2153 rule 5 it counts as "not run". It may be rerun unchanged once the other CamSpec jobs have finished (crash fix only; model C is not in the W-vs-L tally).
