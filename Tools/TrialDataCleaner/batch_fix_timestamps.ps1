echo hello

$files = Get-ChildItem -Path "..\Replayed" -Name

for ($i=0; $i -lt $files.Count; $i++) {
     
    #echo $(Get-Content $files[$i].FullName) #| Where-Object { ($_ -match 'step4' -or $_ -match 'step9') } | Set-Content $outfile
    echo "Cleaning file $i"
    echo $files[$i]
    $infile = "..\Replayed\"+$files[$i]
    $outString = $files[$i] -replace "Vers-Replayed", "Vers-2"
    
    echo $infile

    $outfile= "..\TimeCorrected\" + $outString 
    echo $outfile

    $command = "python .\fix_timestamps.py $infile $outfile"

    invoke-expression -Command $command
}

pause