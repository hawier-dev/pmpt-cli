[Setup]
AppId={{8B5A3F2D-1C4E-4F7A-9B8D-2E6C3A1F5E9B}
AppName=PMPT CLI
AppVersion=0.1.2
AppPublisher=hawier-dev
AppPublisherURL=https://github.com/hawier-dev/pmpt-cli
AppSupportURL=https://github.com/hawier-dev/pmpt-cli/issues
AppUpdatesURL=https://github.com/hawier-dev/pmpt-cli/releases
DefaultDirName={autopf}\PMPT CLI
DefaultGroupName=PMPT CLI
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=dist\installer
OutputBaseFilename=pmpt-setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ChangesEnvironment=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\pmpt.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\PMPT CLI"; Filename: "{app}\pmpt.exe"; Parameters: "--help"
Name: "{group}\{cm:UninstallProgram,PMPT CLI}"; Filename: "{uninstallexe}"

[Registry]
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Check: NeedsAddPath('{app}')

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  Result := Pos(';' + UpperCase(Param) + ';', ';' + UpperCase(OrigPath) + ';') = 0;
end;

[Run]
Filename: "{app}\pmpt.exe"; Parameters: "version"; Flags: runhidden waituntilterminated; Description: "Test installation"

[UninstallDelete]
Type: files; Name: "{app}\pmpt.exe"