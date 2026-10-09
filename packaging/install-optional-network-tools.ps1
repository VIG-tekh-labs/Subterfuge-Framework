# Optional, owner-selected post-install setup via Windows Package Manager.
# Downloads only from the user's configured WinGet repositories.
# Network access, agreements, OS drivers and elevated privileges may be needed.
$ErrorActionPreference = 'Stop'
$logDir = Join-Path $env:LOCALAPPDATA 'Subterfuge'
New-Item -Path $logDir -ItemType Directory -Force | Out-Null
$log = Join-Path $logDir 'optional-network-tools-install.log'
$failed = New-Object System.Collections.Generic.List[string]
$packages = @(
  @{ ID = 'Insecure.Nmap'; Name = 'Nmap'; Exe = 'nmap.exe' },
  @{ ID = 'WiresharkFoundation.Wireshark'; Name = 'Wireshark / TShark'; Exe = 'tshark.exe' },
  @{ ID = 'mitmproxy.mitmproxy'; Name = 'mitmproxy'; Exe = 'mitmdump.exe' }
)
function Write-Log([string]$message) {
    $line = "[$(Get-Date -Format s)] $message"
    Write-Host $line
    Add-Content -Path $log -Value $line -Encoding UTF8
}
Write-Log 'Optional network tooling installation requested.'
$winget = Get-Command winget.exe -ErrorAction SilentlyContinue
if ($null -eq $winget) {
    Write-Log 'WinGet is unavailable. Main Subterfuge app remains installed.'
    Write-Log 'Enable Windows Package Manager, then rerun this optional script.'
    exit 2
}
foreach ($package in $packages) {
    try {
        $existing = Get-Command $package.Exe -ErrorAction SilentlyContinue
        if ($null -ne $existing) {
            Write-Log "$($package.Name): available on PATH."
            continue
        }
        Write-Log "$($package.Name): installing through configured WinGet sources."
        $arguments = @(
          'install', '--id', $package.ID, '--exact', '--silent',
          '--accept-source-agreements', '--accept-package-agreements',
          '--disable-interactivity'
        )
        & $winget.Source @arguments 2>&1 | ForEach-Object { Write-Log "$_" }
        if ($LASTEXITCODE -ne 0) {
            $failed.Add("$($package.Name): WinGet returned $LASTEXITCODE")
        } else {
            Write-Log "$($package.Name): installation command finished."
        }
    } catch {
        $failed.Add("$($package.Name): $($_.Exception.Message)")
    }
}
if ($failed.Count -gt 0) {
    foreach ($message in $failed) { Write-Log $message }
    Write-Log 'Some optional tools failed; core GUI and offline analysis remain installed.'
    exit 1
}
Write-Log 'Optional network package installation complete.'
Write-Log 'Reload PATH/new session as necessary; packet capture drivers may need separate consent.'
exit 0
