echo hello

$files = Get-ChildItem -Path "..\SourceFolder" -Name

for ($i=0; $i -lt $files.Count; $i++) {
     
    #echo $(Get-Content $files[$i].FullName) #| Where-Object { ($_ -match 'step4' -or $_ -match 'step9') } | Set-Content $outfile
    echo "Cleaning file $i"
    echo $files[$i]
    $infile = "..\SourceFiles\"+$files[$i]
    $outString = $files[$i] -replace "Vers-Replayed", "Vers-3"
    
    echo $infile

    $outfile= "..\DestinationFolder\" + $outString 
    echo $outfile

    $command = "python .\clean_data_strip_acs.py $infile $outfile"

    invoke-expression -Command $command
}

pause
