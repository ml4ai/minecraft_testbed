Write-Output hello

$inPath = ".\NoAdvisorTrials\Stripped_Version_6\202\"
$outPath = ".\NoAdvisorTrials\Stripped_Version_7\202\"

$files = Get-ChildItem -Path $inPath -Name
for ($i=0; $i -lt $files.Count; $i++) {     
    
    Write-Output "Cleaning file $i"
    Write-Output $files[$i]
    $infile = $inPath+$files[$i]
    $outString = $files[$i] -replace "Vers-6-Stripped", "Vers-6-Stripped_Ids"    
    Write-Output $infile

    $outfile= $outPath + $outString 
    Write-Output $outfile

    $command = "python .\correct_ids.py $infile $outfile"

    invoke-expression -Command $command
}

pause
