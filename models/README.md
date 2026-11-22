# Reference transistor model

Obtain `16nm_HP.pm` directly from the CMU-SAFARI CROW repository. The card specifies separate NMOS and PMOS models, BSIM4 level 54, nominal 0.7 V, and nominal temperature 27 °C. The testbench uses drawn lengths of 16 nm, NMOS width 32 nm and PMOS width 64 nm. These widths were chosen in the supplied circuit. [CROW model](https://github.com/CMU-SAFARI/CROW/blob/master/SPICESim/PTM_transistors/HP/16nm_HP.pm)

From the repository root in PowerShell, on a fresh clone:

```powershell
$card = 'simulations/ff-timing/16nm_HP.pm'
Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/CMU-SAFARI/CROW/master/SPICESim/PTM_transistors/HP/16nm_HP.pm' -OutFile $card
(Get-FileHash -Algorithm SHA256 -LiteralPath $card).Hash
```

Expected SHA-256: `72F9972D36A9E606785DAC9B6F0CE11F07745CF012B2F9229AC3934CAD9E87B0`. The model used for the baseline matched the upstream file byte for byte. The runner checks this fingerprint before simulation.

CROW requests citation of its associated work (Hassan et al., ISCA 2019). The card contains no license notice and the reviewed upstream material did not establish model-specific redistribution permission. Git ignores the downloaded card and ZIP archives. This repository does not grant rights to the third-party model. [CROW attribution](https://github.com/CMU-SAFARI/CROW)

The academic PTM catalog treats bulk CMOS and multigate FinFET families separately. This project's 16 nm bulk card is sourced specifically from CROW. Official TSMC N16 FinFET technology is outside the scope of this experiment. [Academic PTM catalog](https://mec.umn.edu/ptm)
