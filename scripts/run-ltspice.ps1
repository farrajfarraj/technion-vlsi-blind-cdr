param(
    [string]$LTspice = "$env:LOCALAPPDATA\Programs\ADI\LTspice\LTspice.exe"
)
$ErrorActionPreference = 'Stop'
$bench = Join-Path $PSScriptRoot '../simulations/ff-timing'
$model = Join-Path $bench '16nm_HP.pm'
$expected = '72F9972D36A9E606785DAC9B6F0CE11F07745CF012B2F9229AC3934CAD9E87B0'
if (!(Test-Path -LiteralPath $model) -or (Get-FileHash -LiteralPath $model).Hash -ne $expected) {
    throw 'The reference model is missing or differs. See models/README.md.'
}
if (!(Test-Path -LiteralPath $LTspice)) {
    throw 'Pass the installed LTspice.exe path using -LTspice.'
}
$decks = @(
    '00_device_dc.cir'
    '01_inverter_16nm_BSIM4.cir'
    '01_inverter_schematic.asc'
    '02_flipflop_function.cir'
    '03_flipflop_setup.cir'
    '04_flipflop_setup_refined.cir'
    '05_flipflop_setup_fine.cir'
)
foreach ($deck in $decks) {
    $flags = @('-b')
    if ($deck -match '^(00|01|02)_') { $flags += '-ascii' }
    if ($deck.EndsWith('.asc')) { $flags += '-Run' }
    Write-Output "Running $deck"
    $run = Start-Process -FilePath $LTspice -WorkingDirectory $bench -ArgumentList ($flags + $deck) -WindowStyle Hidden -PassThru -Wait
    if ($run.ExitCode -ne 0) {
        throw "LTspice exited with code $($run.ExitCode) for $deck. Inspect its .log in simulations/ff-timing."
    }
}
