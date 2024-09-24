$files = Get-ChildItem -Path ".\Metadata" -Name

for ($i=0; $i -lt $files.Count; $i++) {
     
    #echo $(Get-Content $files[$i].FullName) #| Where-Object { ($_ -match 'step4' -or $_ -match 'step9') } | Set-Content $outfile
    echo "Cleaning file $i"
    echo $files[$i]
    $infile = ".\Metadata\"+$files[$i]
    $outString = $files[$i] -replace "Vers-1", "AgentQC"
    
    echo $infile

    $outfile= ".\QCFiles\" + $outString 
    echo $outfile

    $command = "python .\run_agent_tests.py $infile $outfile"

    invoke-expression -Command $command
}

pause