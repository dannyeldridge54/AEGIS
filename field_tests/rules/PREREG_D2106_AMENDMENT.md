# D2106 AMENDMENT (Danny 08:49: "your pulses start from one point; start at the furthest point we have")

- Bands now **start at the furthest point reached**: D2105 covers up to L = 5 on G12. So the cloud torus restarts at **B4 (L = 6, Q = 5)**, and Danny's PC (a 2-core VM) runs **B5 (L = 6, Q = 6)** and beyond.
- Each machine keeps its own catalogue; merges happen in the cloud.
- The IN phase still re-tests every catalogued model of that machine.
- The partial B1 cloud run (started 08:44) is stopped. Its catalogue lines are kept as a record.
- Code: START_BAND and TORUS_DIR environment variables only. Filters, goalposts and the stop rule are unchanged.
- **Addendum (08:55):** the device VM kills background jobs at the end of each call, so the PC run moves to native Windows. A SHARD = i/n environment variable splits OUT-1's χ list round-robin across processes (one per core), each with its own TORUS_DIR. TORUS_MINUTES sets each process's time slice. Filters, goalposts and the stop rule are unchanged; the shard catalogues are merged in the cloud.
