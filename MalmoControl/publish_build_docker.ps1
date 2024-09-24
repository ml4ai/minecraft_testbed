New-Variable -Name "date" -Visibility Public -Value $(Get-Date)
echo $date
dotnet publish ./MalmoControl
docker build -t malmocontrol:latest --build-arg CACHE_BREAKER=$date .