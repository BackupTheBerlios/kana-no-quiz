; This is the ``Inno setup" script for generating Kana no quiz's all-in-one

; Windows installer which thus provides  the program and all its dependencies

; (Python interpreter with required modules, and the Windows port of the GTK+

; library as well).



[Setup]

AppName=Kana no quiz

AppVerName=Kana no quiz v1.9.5

AppPublisher=Choplair-Network

AppPublisherURL=http://www.choplair.org/

DefaultDirName={pf}\Choplair-Network\Kana-no-quiz

DefaultGroupName=Kana no quiz

DisableProgramGroupPage=true

OutputBaseFilename=setup

Compression=lzma

SolidCompression=true

AllowUNCPath=false

VersionInfoVersion=1.9.5

VersionInfoCompany=Choplair-Network

VersionInfoDescription=Kana no quiz

LicenseFile=dist\share\kana-no-quiz\GPL.txt

ShowLanguageDialog=yes



[Languages]

Name: "en"; MessagesFile: "compiler:Default.isl"

Name: "es"; MessagesFile: "compiler:Languages\Spanish.isl"

Name: "de"; MessagesFile: "compiler:Languages\German.isl"

Name: "fr"; MessagesFile: "compiler:Languages\French.isl"

Name: "pt_BR"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

Name: "ru"; MessagesFile: "compiler:Languages\Russian.isl"



[Dirs]

Name: {app}; Flags: uninsalwaysuninstall;



[Files]

Source: dist\*; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs



[Icons]

Name: {group}\Kana no quiz v1.9.5; Filename: {app}\kana-no-quiz.exe; WorkingDir: {app}; IconFilename: "{app}\share\kana-no-quiz\img\icon.ico"

Name: "{group}\Uninstall Kana no quiz v1.9.5"; Filename: "{uninstallexe}"



[Run]

Filename: {app}\kana-no-quiz.exe; Description: {cm:LaunchProgram,Kana no quiz}; Flags: nowait postinstall skipifsilent

