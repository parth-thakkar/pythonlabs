# Set-DisplayScalingTo100.ps1
# Run as standard user - no admin required
# Works on Windows 11 (tested in various reports up to 2025)

param(
    [int]$OverrideValue = -2  # -2 forces 100% reliably on most Win11 systems
                              # Try 0 first if you want "system default" (often not 100%)
)

$source = @'
using System;
using System.Runtime.InteropServices;

public class DPIOverride
{
    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool SystemParametersInfo(uint uiAction, uint uiParam, IntPtr pvParam, uint fWinIni);

    public const uint SPI_SETLOGICALDPIOVERRIDE = 0x009F;
    public const uint SPIF_UPDATEINIFILE = 0x01;
}
'@

Add-Type -TypeDefinition $source -ErrorAction Stop

# Cast to uint (handles negative -2 as large positive for override)
$scaling = [uint][int]$OverrideValue

$result = [DPIOverride]::SystemParametersInfo(
    [DPIOverride]::SPI_SETLOGICALDPIOVERRIDE,
    $scaling,
    [IntPtr]::Zero,
    [DPIOverride]::SPIF_UPDATEINIFILE
)

if ($result) {
    Write-Host "Display scaling forced to 100% successfully!" -ForegroundColor Green
    Write-Host "Changes should apply immediately. Move/resize some windows if text looks off initially."
} else {
    Write-Host "Failed to set scaling. Try running with -OverrideValue 0 or check if restricted by policy." -ForegroundColor Red
}