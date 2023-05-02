<#
.SYNOPSIS
    Recursively renames files and folders containing invalid characters for Windows file systems and zip files.

.DESCRIPTION
    This script searches for files and folders with invalid characters in their names, and replaces those characters
    with a safe alternative (underscore). This resolves issues with zipping and syncing to OneDrive, as well as ensuring
    compatibility with the Windows file system.

.EXAMPLE
    To run the script, simply execute it in a PowerShell window. The script will use the current working directory as
    the root path for renaming files and folders.
#>

function Sanitize-FileName {
    <#
    .SYNOPSIS
        Sanitizes a file or folder name by replacing invalid characters with underscores.

    .DESCRIPTION
        This function takes a file or folder name as input, and replaces any invalid characters for Windows file systems,
        zip files, and non-ASCII characters with underscores.

    .PARAMETER FileName
        The file or folder name to be sanitized.

    .EXAMPLE
        $sanitizedFileName = Sanitize-FileName -FileName $originalFileName
    #>
    param (
        [string]$FileName
    )

    # Combine invalid characters for Windows file system and zip files
    $invalidChars = [IO.Path]::GetInvalidFileNameChars() -join ''
    $zipInvalidChars = ":*?|—"
    $regex = "[{0}{1}]" -f [RegEx]::Escape($invalidChars), [RegEx]::Escape($zipInvalidChars)

    # Replace invalid characters with underscores
    $sanitizedFileName = $FileName -replace $regex, '_'

    # Replace non-ASCII characters with underscores
    $sanitizedFileName = $sanitizedFileName -replace '[^\x00-\x7F]', '_'

    return $sanitizedFileName
}

function Rename-InvalidFileAndFolderNames {
    <#
    .SYNOPSIS
        Recursively renames files and folders containing invalid characters in a given path.

    .DESCRIPTION
        This function takes a path as input, and recursively renames all files and folders within that path, replacing
        invalid characters with underscores.

    .PARAMETER Path
        The path to the folder where the renaming process should start.

    .EXAMPLE
        Rename-InvalidFileAndFolderNames -Path $rootPath -Verbose
    #>
    param (
        [string]$Path
    )

    # Recursively process files and folders within the given path
    Get-ChildItem -Path $Path -Recurse -Force | ForEach-Object {
        if ($_.Name -ne (Sanitize-FileName $_.Name)) {
            $newName = Sanitize-FileName $_.Name
            $newPath = Join-Path $_.Directory.FullName $newName

            if (-not (Test-Path $newPath)) {
                Rename-Item -Path $_.FullName -NewName $newName -Force
                Write-Host "Renamed $($_.FullName) to $newPath"
            } else {
                Write-Warning "Unable to rename $($_.FullName) to $newPath. A file or folder with the same name already exists."
            }
        }
    }
}

# Set the root path to the current working directory
$rootPath = Get-Location

# Call the function to rename files and folders with invalid characters
Rename-InvalidFileAndFolderNames -Path $rootPath -Verbose
