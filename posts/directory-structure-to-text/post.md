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

    <div class="codehilite mt-4">
        <pre><code id="output">Output will appear here after selecting a directory.</code></pre>
    </div>
</div>

<div id="unsupported-alert" class="alert alert-danger" style="display: none" role="alert">
  Sorry, your browser is not supported as this uses <a href="https://web.dev/file-system-access/">the File System Access API</a>
</div>


<script>
    const selectDirectoryElementId = "select-directory";
    const outputElementId = "output";
    const excludeFilterElementId = "exclude-filter";
    const ignoreEmptyFoldersElementId = "ignore-empty-folders";

    const getFilesAndDirNodeForHandle = async (dirHandle, currentPath = '') => {
        const nodesPath = currentPath + '/' + dirHandle.name;
        console.log(`[Search] ${nodesPath}`);

        const node = {
            name: dirHandle.name,
            kind: dirHandle.kind,
            handle: dirHandle,
            children: [],
            path: nodesPath
        };

        // If this node is a directory, search for subdirectories and files
        if (node.kind === "directory") {
            for await (const [_, handle] of dirHandle) {
                node.children.push(await getFilesAndDirNodeForHandle(handle, nodesPath));
            }
        }

        // Order the child nodes after discovery
        node.children.sort((a, b) => {
            if (a.kind === "directory" && b.kind === "file") {
                return -1;
            }
            if (a.kind === "file" && b.kind === "directory") {
                return 1;
            }
            return a.name.localeCompare(b.name);
        });

        return node;
    };

    const filterNode = (node, excludeFilterRegex = null, ignoreEmptyFolders = false) => {
        const filteredChildren = [];
        for (const child of node.children) {
            const filteredChild = filterNode(child, excludeFilterRegex, ignoreEmptyFolders);
            if (filteredChild !== null) {
                filteredChildren.push(filteredChild);
            }
        }
        node.children = filteredChildren; // Warning, mutable

        if (ignoreEmptyFolders && node.kind === "directory" && node.children.length === 0) {
            console.log(`[Filter] Removed ${node.path} as it is empty`);
            return null;
        }

        if (excludeFilterRegex !== null && excludeFilterRegex.test(node.path)) {
            console.log(`[Filter] Removed ${node.path} as it matched the regex`);
            return null;
        }

        return node;
    }

    const getStructureDisplay = (node, indentationText = "") => {
        let structureDisplay = "";

        // Render the node
        structureDisplay += `📁 ${node.name}\n`;

        // Render the children
        for (const [index, child] of node.children.entries()) {
            const isLastChild = index === node.children.length - 1;
            const directoryPipe = isLastChild ? "┗ " : "┣ ";

            if (child.kind === "directory") {
                const newIndentationText =
                    indentationText + (isLastChild ? "  " : "┃ ");
                const childDisplay = getStructureDisplay(child, newIndentationText);
                structureDisplay += `${indentationText}${directoryPipe}${childDisplay}`;
            }
            if (child.kind === "file") {
                structureDisplay += `${indentationText}${directoryPipe}📜 ${child.name}\n`;
            }
        }

        return structureDisplay;
    };

    const onSelectDirectory = async () => {
        const dirHandle = await window.showDirectoryPicker();
        console.log(`[Search] Starting search`);
        const node = await getFilesAndDirNodeForHandle(dirHandle, '');
        console.log(`[Search] Search ended`);
        console.log(`[Search] Search results`, node);

        console.log(`[Filter] Starting filter`);
        const excludeFilterElement = document.getElementById(excludeFilterElementId);
        const excludeFilter = excludeFilterElement.value === '' ? null : new RegExp(excludeFilterElement.value, "m");
        const ignoreEmptyFolders = document.getElementById(ignoreEmptyFoldersElementId).checked;
        const filteredNode = filterNode(node, excludeFilter, ignoreEmptyFolders);
        console.log(`[Filter] Filter ended`);
        console.log(`[Filter] Filter results`, filteredNode);

        console.log(`[Display] Starting display`);
        const display = getStructureDisplay(filteredNode);
        const outputElement = document.getElementById(outputElementId);
        outputElement.innerText = display;
        console.log(`[Display] Ended display`);
    };

    // When the page first loads, hook everything up
    document.addEventListener("DOMContentLoaded", () => {
        const doesBrowserSupportSpecialFeatures = typeof window.showDirectoryPicker !== undefined;
        if (doesBrowserSupportSpecialFeatures) {
            const selectDirectoryElement = document.getElementById(
                selectDirectoryElementId
            );
            selectDirectoryElement.addEventListener("click", onSelectDirectory);
        } else {
            document.getElementById("tool").style.display = "none";
            document.getElementById("unsupported-alert").style.display = "block";
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
        const outputElement = document.getElementById(outputElementId);
        outputElement.innerText = preMessage;
    });
</script>