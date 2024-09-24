New-Variable -Name "date" -Visibility Public -Value $(Get-Date)
echo $date
cd .\AngularApp\ClientMap
ng build --prod
cd ..\..\
docker build -t client_map --build-arg CACHE_BREAKER=$date .
