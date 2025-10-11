title: "Directory Structure to Text"
date: 2022-08-10
category: Tools
tags: [documentation, tool]
feature: feature.png
description: "This is a tool where you can select a file on your PC and it will be rendered into text to then be used for documentation. This is super useful for annotating project file structures."

<div id="tool">
    <div class="row">
        <div class="col">
            <div class="input-group">
                <div class="input-group-prepend">
                    <span class="input-group-text" id="filter-label">Exclude Filter</span>
                </div>
                <input id="exclude-filter" type="text" class="form-control" placeholder="Regex (matching paths are ignored)" aria-describedby="filter-label">
            </div>
            <div class="form-check mt-2">
                <input type="checkbox" class="form-check-input" id="ignore-empty-folders">
                <label class="form-check-label" for="ignore-empty-folders">Ignore empty folders</label>
            </div>
        </div>

        <div class="col-sm-auto mt-2 mt-sm-0 text-center">
            <button id="select-directory" type="button" class="btn btn-outline-primary">📁 Select Directory</button>
        </div>
    </div>

    <div class="mt-4">
        <div id="copy-output-wrapper" class="mb-1 d-none justify-content-end">
            <button id="copy-output" type="button" class="btn btn-primary">📋 Copy Output</button>
        </div>
        <div class="codehilite">
            <pre><code id="output">Output will appear here after selecting a directory.</code></pre>
        </div>
    </div>
</div>

<div id="unsupported-alert" class="alert alert-danger" style="display: none" role="alert">
  Sorry, your browser is not supported as this uses <a href="https://web.dev/file-system-access/">the File System Access API</a>
</div>


<script>
    // Get all required element references up front
    const toolElement = document.getElementById("tool");
    const unsupportedAlertElement = document.getElementById("unsupported-alert");
    const selectDirectoryElement = document.getElementById("select-directory");
    const outputElement = document.getElementById("output");
    const excludeFilterElement = document.getElementById("exclude-filter");
    const ignoreEmptyFoldersElement = document.getElementById("ignore-empty-folders");
    const copyOutputWrapperElement = document.getElementById("copy-output-wrapper");
    const copyOutputElement = document.getElementById("copy-output");

    const getFilesAndDirNodeForHandle = async (dirHandle, currentPath = '', excludeFilterRegex = null, ignoreEmptyFolders = false) => {
        const nodesPath = currentPath + '/' + dirHandle.name;

        // Skip if the current path matches the exclude regex
        if (excludeFilterRegex && excludeFilterRegex.test(nodesPath)) {
            console.log(`[Search][Skipping] ${nodesPath} (excluded by regex)`);
            return null;
        }

        console.log(`[Search] ${nodesPath}`);

        const node = {
            name: dirHandle.name,
            kind: dirHandle.kind,
            handle: dirHandle,
            children: [],
            path: nodesPath
        };

        if (node.kind === "directory") {
            for await (const [_, handle] of dirHandle) {
                const childNode = await getFilesAndDirNodeForHandle(handle, nodesPath, excludeFilterRegex, ignoreEmptyFolders);
                if (childNode !== null) {
                    node.children.push(childNode);
                }
            }

            // Ignore empty directories if the user requested
            if (ignoreEmptyFolders && node.children.length === 0) {
                console.log(`[Search][Skipping] ${nodesPath} (empty folder)`);
                return null;
            }

            // Sort folders before files alphabetically
            node.children.sort((a, b) => {
                if (a.kind === "directory" && b.kind === "file") return -1;
                if (a.kind === "file" && b.kind === "directory") return 1;
                return a.name.localeCompare(b.name);
            });
        }

        return node;
    };

    const getStructureDisplay = (node, indentationText = "") => {
        let structureDisplay = "";

        // Render the node
        structureDisplay += `📁 ${node.name}\n`;

        // Render the children
        for (const [index, child] of node.children.entries()) {
            const isLastChild = index === node.children.length - 1;
            const directoryPipe = isLastChild ? "┗ " : "┣ ";

            if (child.kind === "directory") {
                const newIndentationText = indentationText + (isLastChild ? "  " : "┃ ");
                const childDisplay = getStructureDisplay(child, newIndentationText);
                structureDisplay += `${indentationText}${directoryPipe}${childDisplay}`;
            } else if (child.kind === "file") {
                structureDisplay += `${indentationText}${directoryPipe}📜 ${child.name}\n`;
            }
        }

        return structureDisplay;
    };

    const onSelectDirectory = async () => {
        const dirHandle = await window.showDirectoryPicker();

        const excludeFilter = excludeFilterElement.value === '' ? null : new RegExp(excludeFilterElement.value, "m");
        const ignoreEmptyFolders = ignoreEmptyFoldersElement.checked;

        console.log(`[Search] Starting search`);
        const rootNode = await getFilesAndDirNodeForHandle(dirHandle, '', excludeFilter, ignoreEmptyFolders);
        console.log(`[Search] Search ended`);
        console.log(`[Search] Search results`, rootNode);

        console.log(`[Display] Starting display`);
        const display = getStructureDisplay(rootNode);
        outputElement.innerText = display;
        console.log(`[Display] Ended display`);

        // Show the copy button
        copyOutputWrapperElement.classList.remove("d-none");
        copyOutputWrapperElement.classList.add("d-flex");
    };

    const onCopyOutput = async () => {
        const outputText = outputElement.innerText;
        try {
            await navigator.clipboard.writeText(outputText);

            const originalText = copyOutputElement.innerText;
            copyOutputElement.innerText = "✅ Copied!";
            copyOutputElement.disabled = true;

            setTimeout(() => {
                copyOutputElement.innerText = originalText;
                copyOutputElement.disabled = false;
            }, 1500);
        } catch (err) {
            alert("Failed to copy to clipboard: " + err);
        }
    };

    // When the page first loads, hook everything up
    document.addEventListener("DOMContentLoaded", () => {
        const doesBrowserSupportSpecialFeatures = typeof window.showDirectoryPicker !== undefined;
        if (doesBrowserSupportSpecialFeatures) {
            selectDirectoryElement.addEventListener("click", onSelectDirectory);
            copyOutputElement.addEventListener("click", onCopyOutput);
        } else {
            toolElement.style.display = "none";
            unsupportedAlertElement.style.display = "block";
        }

        const preMessage = "Output will appear here after selecting a directory."
            + "\n"
            + "\nAn exclude filter can be added to ignore files or folders."
            + "\n  - Folder paths look like: /folder selected/nested"
            + "\n  - File paths look like: /folder selected/folder1/folder2/file.png"
            + "\nYou can use a regex to ignore certain directory names or file types."
            + "\nLook in the console to see the folders/files found to see their paths."
            + "\n"
            + "\nDetails about your files are kept on your machine.";
        outputElement.innerText = preMessage;
    });
</script>

## Example Filters

These are some example filters for specific project types

### Python

Ignore `.git`, `.venv`, `__pycache__`, `.idea`

```
(^|\/)(?:\.git|.venv|__pycache__|.idea)(?:\/|$)
```

### C\#

Ignore `.git`, `.vs`, `bin`, `obj`

```
(^|\/)(?:\.git|.vs|bin|obj)(?:\/|$)
```

### Node/JavaScript

Ignore `.git`, `node_modules`, `build`, `dist`

```
(^|\/)(?:\.git|node_modules|build|dist)(?:\/|$)
```