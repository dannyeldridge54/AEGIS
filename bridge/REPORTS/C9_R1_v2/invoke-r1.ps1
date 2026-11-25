$ErrorActionPreference = 'Stop'
$Python = Join-Path ([Environment]::GetFolderPath('LocalApplicationData')) 'Programs\Python\Python312\python.exe'
$Names = @('r1-stdout-v2.txt', 'r1-stderr-v2.txt', 'r1-execution-v2.json',
           'r1-started-v2.json', 'r1-result-v2.json')
foreach ($Name in $Names) {
    if (Test-Path -LiteralPath (Join-Path $PSScriptRoot $Name)) {
        throw "Refusing an existing R1 output: $Name"
    }
}
$Streams = @()
$Record = [ordered]@{ case = 'R1'; process_started = $false; exit_code = 1 }
$Watch = [Diagnostics.Stopwatch]::StartNew()
try {
    foreach ($Name in $Names[0..2]) {
        $Streams += [IO.File]::Open((Join-Path $PSScriptRoot $Name),
            [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::Read)
    }
    $Info = New-Object Diagnostics.ProcessStartInfo
    $Info.FileName = $Python
    $Info.Arguments = '-I -B -u "' + (Join-Path $PSScriptRoot 'r1.py') + '"'
    $Info.WorkingDirectory = $PSScriptRoot
    $Info.UseShellExecute = $false
    $Info.RedirectStandardOutput = $true
    $Info.RedirectStandardError = $true
    $Process = New-Object Diagnostics.Process
    $Process.StartInfo = $Info
    if (-not $Process.Start()) { throw 'Python process did not start' }
    $Record.process_started = $true
    $Record.process_id = $Process.Id
    $OutTask = $Process.StandardOutput.BaseStream.CopyToAsync($Streams[0])
    $ErrTask = $Process.StandardError.BaseStream.CopyToAsync($Streams[1])
    $Process.WaitForExit()
    $OutTask.GetAwaiter().GetResult()
    $ErrTask.GetAwaiter().GetResult()
    $Record.exit_code = $Process.ExitCode
} catch {
    $Record.error = [ordered]@{ type = $_.Exception.GetType().FullName; message = $_.Exception.Message }
    [Console]::Error.WriteLine($_.Exception.Message)
} finally {
    $Watch.Stop()
    $Record.elapsed_seconds = $Watch.Elapsed.TotalSeconds
    $Record.python_executable_sha256 = (Get-FileHash -LiteralPath $Python -Algorithm SHA256).Hash.ToLowerInvariant()
    for ($i = 0; $i -lt [Math]::Min(2, $Streams.Count); $i++) { $Streams[$i].Dispose() }
    if ($Streams.Count -eq 3) {
        $Record.stdout_sha256 = (Get-FileHash -LiteralPath (Join-Path $PSScriptRoot $Names[0]) -Algorithm SHA256).Hash.ToLowerInvariant()
        $Record.stderr_sha256 = (Get-FileHash -LiteralPath (Join-Path $PSScriptRoot $Names[1]) -Algorithm SHA256).Hash.ToLowerInvariant()
        $Result = Join-Path $PSScriptRoot 'r1-result-v2.json'
        if (Test-Path -LiteralPath $Result) {
            $Record.result_sha256 = (Get-FileHash -LiteralPath $Result -Algorithm SHA256).Hash.ToLowerInvariant()
        }
        $Text = ($Record | ConvertTo-Json -Depth 6) + "`n"
        $Bytes = (New-Object Text.UTF8Encoding($false)).GetBytes($Text)
        $Streams[2].Write($Bytes, 0, $Bytes.Length)
        $Streams[2].Dispose()
    }
}
$Record | ConvertTo-Json -Depth 6
exit $Record.exit_code
