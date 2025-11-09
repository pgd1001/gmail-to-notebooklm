; Gmail to NotebookLM - Inno Setup Installer Script
; Requires Inno Setup 6.0 or later: https://jrsoftware.org/isinfo.php

#define MyAppName "Gmail to NotebookLM"
#define MyAppVersion "0.4.0"
#define MyAppPublisher "Paul Deegan"
#define MyAppURL "https://github.com/pgd1001/gmail-to-notebooklm"
#define MyAppExeName "g2n-gui.exe"
#define MyAppExeCLI "g2n.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{8E3F4A2B-9C5D-4F1E-B8A7-6D9E2C1F0B3A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=LICENSE
OutputDir=installer_output
OutputBaseFilename=gmail-to-notebooklm-setup-{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}
SetupIconFile=

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "addtopath"; Description: "Add to PATH (allows running g2n and g2n-gui from command line)"; GroupDescription: "System Integration:"

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\{#MyAppExeCLI}"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "QUICKSTART.md"; DestDir: "{app}"; Flags: ignoreversion; AfterInstall: AfterInstallProc
Source: "SIMPLIFIED_SETUP.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "ADVANCED_SETUP.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "BETA_ACCESS.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "SETUP_WINDOWS.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "USAGE.md"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Code]
const
    EnvironmentKey = 'Environment';

procedure AfterInstallProc;
begin
    // Placeholder for post-install actions
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
    Path: string;
    AppDir: string;
begin
    if (CurStep = ssPostInstall) and WizardIsTaskSelected('addtopath') then
    begin
        AppDir := ExpandConstant('{app}');

        // Get current user PATH
        if RegQueryStringValue(HKEY_CURRENT_USER, EnvironmentKey, 'Path', Path) then
        begin
            // Check if already in PATH
            if Pos(Uppercase(AppDir), Uppercase(Path)) = 0 then
            begin
                // Add to PATH
                if Path <> '' then
                    Path := Path + ';';
                Path := Path + AppDir;

                // Save to registry
                if RegWriteStringValue(HKEY_CURRENT_USER, EnvironmentKey, 'Path', Path) then
                begin
                    MsgBox('The application directory has been added to your PATH.' + #13#10 +
                           'You may need to restart your terminal for the changes to take effect.',
                           mbInformation, MB_OK);
                end;
            end;
        end;
    end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
    Path: string;
    AppDir: string;
    P: Integer;
begin
    if CurUninstallStep = usPostUninstall then
    begin
        AppDir := ExpandConstant('{app}');

        // Remove from PATH
        if RegQueryStringValue(HKEY_CURRENT_USER, EnvironmentKey, 'Path', Path) then
        begin
            P := Pos(Uppercase(AppDir), Uppercase(Path));
            if P > 0 then
            begin
                // Remove the directory from PATH
                Delete(Path, P, Length(AppDir));

                // Remove trailing semicolon if present
                if (P <= Length(Path)) and (Path[P] = ';') then
                    Delete(Path, P, 1);

                // Remove leading semicolon if present
                if (P > 1) and (Path[P-1] = ';') then
                    Delete(Path, P-1, 1);

                // Save back to registry
                RegWriteStringValue(HKEY_CURRENT_USER, EnvironmentKey, 'Path', Path);
            end;
        end;
    end;
end;

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

