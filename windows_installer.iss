; This is the ``Inno setup" script for generating Kana no quiz's Windows
; installer for the program and all its dependencies (Python interpreter with
; required modules, and the Windows port of the GTK+ library as well).

[Setup]
AppName=Kana no quiz
AppVerName=Kana no quiz v2.0 (CVS)
AppPublisher=Choplair-network
AppPublisherURL=http://www.choplair.org/
DefaultDirName={pf}\Choplair-network\Kana-no-quiz
DefaultGroupName=Kana no quiz
DisableProgramGroupPage=true
OutputBaseFilename=setup
Compression=lzma
SolidCompression=true
AllowUNCPath=false
VersionInfoVersion=2.0
VersionInfoCompany=Choplair-network
VersionInfoDescription=Kana no quiz
LicenseFile=dist\share\kana-no-quiz\GPL.txt
ShowLanguageDialog=yes

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "de"; MessagesFile: "compiler:Languages\German.isl"
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"
Name: "pt_BR"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "ru"; MessagesFile: "compiler:Languages\Russian.isl"

[Dirs]
Name: {app}; Flags: uninsalwaysuninstall;

[Files]
Source: dist\*; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: {group}\Kana no quiz v2.0; Filename: {app}\kana-no-quiz_startup.exe; WorkingDir: {app}; IconFilename: "{app}\share\kana-no-quiz\img\icon.ico"
Name: "{group}\Uninstall Kana no quiz v2.0"; Filename: "{uninstallexe}"

[Run]
Filename: {app}\kana-no-quiz_startup.exe; Description: {cm:LaunchProgram,Kana no quiz}; Flags: nowait postinstall skipifsilent
