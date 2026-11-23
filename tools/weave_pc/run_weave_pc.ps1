# Weave PC runs: D2135 (CamSpec NPIPE, 9 fits) + D2132 w0wa (HiLLiPoP, 3 fits). Each fit is one single-threaded process at BelowNormal priority.
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$py = "C:\Users\Danny\.copilot\repos\AEGIS\cmb-fit\venv312\Scripts\python.exe"
$env:WEAVE_PKGS = "C:\Users\Danny\ufe_data\packages"; $env:OMP_NUM_THREADS = "1"; $env:OPENBLAS_NUM_THREADS = "1"; $env:MKL_NUM_THREADS = "1"
New-Item -ItemType Directory -Force -Path "$here\logs" | Out-Null
$jobs = @()
foreach ($sn in @("desdovekie","pantheonplus","union3")) { foreach ($m in @("L","W","C")) { $jobs += ,@($m,$sn,"camspec") } ; $jobs += ,@("C",$sn,"hillipop") }
foreach ($j in $jobs) {
  $name = "$($j[0])_$($j[1])_$($j[2])"
  $p = Start-Process -FilePath $py -ArgumentList "`"$here\weave_lcdm_pr4.py`" $($j[0]) $($j[1]) $($j[2])" -WorkingDirectory $here `
       -RedirectStandardOutput "$here\logs\$name.out" -RedirectStandardError "$here\logs\$name.err" -WindowStyle Minimized -PassThru
  try { $p.PriorityClass = 'BelowNormal' } catch {}
  Add-Content "$here\logs\launched.txt" "$name pid $($p.Id) $(Get-Date -Format s)"
}
Add-Content "$here\logs\launched.txt" "ALL LAUNCHED $(Get-Date -Format s)"
