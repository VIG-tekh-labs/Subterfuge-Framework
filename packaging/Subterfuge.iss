#define AppName "Subterfuge Framework"
#define AppVersion "2.0.0a5"
#define AppExe "Subterfuge.exe"
[Setup]
AppId={{49A994F0-51C6-4D15-9A35-9FE01B49EE2A}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=Subterfuge contributors
AppPublisherURL=https://github.com/VIG-tekh-labs/Subterfuge-Framework
AppSupportURL=https://github.com/VIG-tekh-labs/Subterfuge-Framework/issues
DefaultDirName={autopf}\Subterfuge Framework
DefaultGroupName=Subterfuge Framework
OutputDir=..\release-assets
OutputBaseFilename=Subterfuge-Setup-2.0.0a5-Windows-x64
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
UninstallDisplayIcon={app}\Subterfuge.exe
SetupIconFile=subterfuge.ico
LicenseFile=..\LICENSE
DisableProgramGroupPage=yes
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked
Name: "networktools"; Description: "Install Nmap, Wireshark/TShark and mitmproxy via WinGet (internet and administrator permission may be needed)"; GroupDescription: "Optional network capabilities:"; Flags: checkedonce
[Files]
Source: "..\dist-frozen\Subterfuge\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "install-optional-network-tools.ps1"; DestDir: "{app}\tools"; Flags: ignoreversion
Source: "..\DESKTOP_GUI.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "..\SERVER_ACCESS.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "..\DOWNLOADS.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "..\THIRD_PARTY_NOTICES.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}\docs"; Flags: ignoreversion
[Icons]
Name: "{autoprograms}\Subterfuge Framework"; Filename: "{app}\{#AppExe}"; WorkingDir: "{app}"
Name: "{autodesktop}\Subterfuge Framework"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon
[Run]
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -File ""{app}\tools\install-optional-network-tools.ps1"""; Description: "Install optional network tools via WinGet"; Tasks: networktools; Flags: waituntilterminated skipifsilent
Filename: "{app}\{#AppExe}"; Description: "Launch Subterfuge Framework"; Flags: nowait postinstall skipifsilent
