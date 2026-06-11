$taskName = "CreativeIntelDailyReport"
$pythonPath = "C:\Python27\python.exe"
$scriptPath = "C:\Users\xuyiqing03\Documents\Codex\2026-06-11\https-smokingarea42-github-io-creative-intel\repo\tools\daily_report.py"
$workDir = "C:\Users\xuyiqing03\Documents\Codex\2026-06-11\https-smokingarea42-github-io-creative-intel\repo"

# Remove existing task
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# Create action with full Python path
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "`"$scriptPath`"" -WorkingDirectory $workDir

# Weekdays at 10:30 AM
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At "10:30"

# Run whether user is logged on or not
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Highest

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description "Creative Intel - auto generate and push daily report" -Force

Write-Host "Task '$taskName' updated with full Python path"
Write-Host "Python: $pythonPath"
Write-Host "Schedule: Monday-Friday at 10:30 AM"
Write-Host ""
Write-Host "=== Task Details ==="
Get-ScheduledTask -TaskName $taskName | Format-List TaskName,State,Description
