@echo off
set jdkUrl=https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jdk/jdk-8u361-windows-x64.zip
set jarUrl=https://github.com/DevsyA/McSkill-Better-Test-Launcher/blob/master/alt/McSkillTest.jar?raw=true
set tempFolder=%TEMP%\McSkillTest
set jdkFileName=%tempFolder%\jdk.zip
set jdkFolder=%tempFolder%\jdk
set jarFileName=%tempFolder%\McSkillTest.jar

if not exist %tempFolder% mkdir %tempFolder%

if not exist %jdkFolder% (
    echo Downloading JDK...
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%jdkUrl%', '%jdkFileName%')"
    echo Extracting JDK...
    powershell Expand-Archive -Path %jdkFileName% -DestinationPath %jdkFolder%
    echo Cleaning up...
    del %jdkFileName%
)

if not exist %jarFileName% (
    echo Downloading Launcher...
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%jarUrl%', '%jarFileName%')"
    echo Download completed.
)

set javaExe=%jdkFolder%\jdk1.8.0_361\bin\java.exe
set jarArgs=-jar "%jarFileName%"
echo Starting Launcher...
start "" "%javaExe%" %jarArgs%