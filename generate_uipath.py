"""
Usage: python generate_uipath.py https://www.google.com
"""

import json, os, sys, uuid, time
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

OUTPUT_DIR = "UiPathProject"

NAMESPACES = [
    "System.Activities","System.Activities.Statements",
    "System.Activities.Expressions","System.Activities.Validation",
    "System.Activities.XamlIntegration","Microsoft.VisualBasic",
    "Microsoft.VisualBasic.Activities","System","System.Collections",
    "System.Collections.Generic","System.Collections.ObjectModel",
    "System.Data","System.Diagnostics","System.Drawing","System.IO",
    "System.Linq","System.Net.Mail","System.Xml","System.Xml.Linq",
    "UiPath.Core","UiPath.Core.Activities","System.Windows.Markup",
    "GlobalVariablesNamespace","GlobalConstantsNamespace",
    "System.Runtime.Serialization","UiPath.UIAutomationNext.Enums",
    "UiPath.UIAutomationCore.Contracts","UiPath.UIAutomationNext.Models",
    "UiPath.UIAutomationNext.Activities","UiPath.Shared.Activities",
    "UiPath.Platform.ObjectLibrary","UiPath.Platform.SyncObjects"
]

REFERENCES = [
    "Microsoft.VisualBasic","mscorlib","PresentationCore",
    "PresentationFramework","System","System.Activities",
    "System.ComponentModel.TypeConverter","System.Core","System.Data",
    "System.Data.Common","System.Data.DataSetExtensions","System.Drawing",
    "System.Drawing.Common","System.Drawing.Primitives","System.Linq",
    "System.Net.Mail","System.ObjectModel","System.Private.CoreLib",
    "System.Xaml","System.Xml","System.Xml.Linq",
    "UiPath.System.Activities","UiPath.UiAutomation.Activities",
    "WindowsBase","UiPath.Studio.Constants","System.Private.ServiceModel",
    "System.Private.DataContractSerialization",
    "System.Runtime.Serialization.Formatters",
    "System.Runtime.Serialization.Primitives","UiPath.UIAutomationNext",
    "UiPath.UIAutomationCore","UiPath.UIAutomationNext.Activities",
    "UiPath.OCR.Activities","UiPath.Platform"
]


def generate_project_json(project_name):
    return {
        "name": project_name,
        "projectId": str(uuid.uuid4()),
        "description": "Blank Process",
        "main": "Main.xaml",
        "dependencies": {
            "UiPath.System.Activities": "[25.12.2]",
            "UiPath.UIAutomation.Activities": "[25.10.26]"
        },
        "webServices": [],
        "entitiesStores": [],
        "schemaVersion": "4.0",
        "studioVersion": "26.0.187.0",
        "projectVersion": "1.0.0",
        "runtimeOptions": {
            "autoDispose": False,
            "netFrameworkLazyLoading": False,
            "isPausable": True,
            "isAttended": False,
            "requiresUserInteraction": True,
            "supportsPersistence": False,
            "workflowSerialization": "NewtonsoftJson",
            "excludedLoggedData": ["Private:*", "*password*"],
            "executionType": "Workflow",
            "readyForPiP": False,
            "startsInPiP": False,
            "mustRestoreAllDependencies": True,
            "pipType": "ChildSession"
        },
        "designOptions": {
            "projectProfile": "Developement",
            "outputType": "Process",
            "libraryOptions": {"privateWorkflows": []},
            "processOptions": {"ignoredFiles": []},
            "fileInfoCollection": [],
            "saveToCloud": False
        },
        "expressionLanguage": "VisualBasic",
        "entryPoints": [{
            "filePath": "Main.xaml",
            "uniqueId": str(uuid.uuid4()),
            "input": [],
            "output": []
        }],
        "isTemplate": False,
        "templateProjectData": {},
        "publishData": {},
        "targetFramework": "Windows"
    }


def generate_main_xaml(url, title, scope_guid):
    ns_lines  = "\n".join([f"      <x:String>{n}</x:String>" for n in NAMESPACES])
    ref_lines = "\n".join([f"      <AssemblyReference>{r}</AssemblyReference>" for r in REFERENCES])

    title_safe = title.replace("'", "*").replace("&", "&amp;")
    url_safe   = url.replace("&", "&amp;")

    return f"""<?xml version="1.0" encoding="utf-8"?>
<Activity mc:Ignorable="sap sap2010" x:Class="Main" VisualBasic.Settings="{{x:Null}}" sap2010:WorkflowViewState.IdRef="ActivityBuilder_1" xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:sap="http://schemas.microsoft.com/netfx/2009/xaml/activities/presentation" xmlns:sap2010="http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation" xmlns:scg="clr-namespace:System.Collections.Generic;assembly=System.Private.CoreLib" xmlns:sco="clr-namespace:System.Collections.ObjectModel;assembly=System.Private.CoreLib" xmlns:sd="clr-namespace:System.Drawing;assembly=System.Drawing.Common" xmlns:sd1="clr-namespace:System.Drawing;assembly=System.Drawing.Primitives" xmlns:uix="http://schemas.uipath.com/workflow/activities/uix" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <TextExpression.NamespacesForImplementation>
    <sco:Collection x:TypeArguments="x:String">
{ns_lines}
    </sco:Collection>
  </TextExpression.NamespacesForImplementation>
  <TextExpression.ReferencesForImplementation>
    <sco:Collection x:TypeArguments="AssemblyReference">
{ref_lines}
    </sco:Collection>
  </TextExpression.ReferencesForImplementation>
  <Sequence DisplayName="Main Sequence" sap:VirtualizedContainerService.HintSize="706,290" sap2010:WorkflowViewState.IdRef="Sequence_1">
    <sap:WorkflowViewStateService.ViewState>
      <scg:Dictionary x:TypeArguments="x:String, x:Object">
        <x:Boolean x:Key="IsExpanded">True</x:Boolean>
      </scg:Dictionary>
    </sap:WorkflowViewStateService.ViewState>
    <uix:NApplicationCard AttachMode="ByInstance" DisplayName="Open browser automation" HealingAgentBehavior="Job" sap:VirtualizedContainerService.HintSize="450,267.3333333333333" sap2010:WorkflowViewState.IdRef="NApplicationCard_1" InteractionMode="DebuggerApi" ScopeGuid="{scope_guid}" Version="V2">
      <uix:NApplicationCard.Body>
        <ActivityAction x:TypeArguments="x:Object">
          <ActivityAction.Argument>
            <DelegateInArgument x:TypeArguments="x:Object" Name="WSSessionData" />
          </ActivityAction.Argument>
          <Sequence DisplayName="Do" sap2010:WorkflowViewState.IdRef="Sequence_2" />
        </ActivityAction>
      </uix:NApplicationCard.Body>
      <uix:NApplicationCard.OCREngine>
        <ActivityFunc x:TypeArguments="sd:Image, scg:IEnumerable(scg:KeyValuePair(sd1:Rectangle, x:String))">
          <ActivityFunc.Argument>
            <DelegateInArgument x:TypeArguments="sd:Image" Name="Image" />
          </ActivityFunc.Argument>
        </ActivityFunc>
      </uix:NApplicationCard.OCREngine>
      <uix:NApplicationCard.TargetApp>
        <uix:TargetApp Area="-11, -11, 1942, 1042" BrowserType="Chrome" ContentHash="rM6clMaW4k2MnokOHv1CFA" IconBase64="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" InformativeScreenshot="8bab349f9de3e0b85a89da128ab46ae1.jpg" Reference="yBsDPg6VG0G9_msFI29EZg/zPpTjBbOcU6SYLnZT-fxkg" Selector="&lt;html app='chrome.exe' title='{title_safe}' /&gt;" Url="{url_safe}" Version="V2" />
      </uix:NApplicationCard.TargetApp>
    </uix:NApplicationCard>
  </Sequence>
</Activity>"""


def main(url):
    parsed       = urlparse(url)
    project_name = parsed.netloc.replace("www.", "").replace(".", "_")
    scope_guid   = str(uuid.uuid4())

    print(f"\n{'='*50}")
    print(f"  UiPath Project Generator")
    print(f"{'='*50}")
    print(f"  URL: {url}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page    = browser.new_page()
        print("  Opening page...")
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(2)
        title = page.title()
        print(f"  Title: {title}")
        browser.close()

    out_dir = os.path.join(OUTPUT_DIR, project_name)
    os.makedirs(out_dir, exist_ok=True)

    # project.json
    proj = generate_project_json(project_name)
    with open(os.path.join(out_dir, "project.json"), "w", encoding="utf-8") as f:
        json.dump(proj, f, indent=2)

    # Main.xaml
    xaml = generate_main_xaml(url, title, scope_guid)
    with open(os.path.join(out_dir, "Main.xaml"), "w", encoding="utf-8") as f:
        f.write(xaml)

    print(f"\n  project.json saved")
    print(f"  Main.xaml saved")
    print(f"\n  Open in UiPath Studio:")
    print(f"  → {out_dir}/project.json")
    print(f"\n{'='*50}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage: python generate_uipath.py <URL>")
        print("Example: python generate_uipath.py https://www.google.com")
        sys.exit(1)
    main(sys.argv[1])