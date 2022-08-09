title: "Directory Structure to Text"
date: 2022-08-10
category: Tools
tags: [documentation, tool]
feature: feature.png
description: "This is a tool where you can select a file on your PC and it will be rendered into text to then be used for documentation. This is super useful for annotating project file structures."

<div id="tool">
    <div class="text-center">
        <button id="select-directory" type="button" class="btn btn-outline-primary">📁 Select Directory</button>
    </div>
    <div class="codehilite mt-4">
        <pre><code id="output">Output will appear here after selecting a directory</code></pre>
    </div>
</div>

<div id="unsupported-alert" class="alert alert-danger" style="display: none" role="alert">
  Sorry, your browser is not supported as this uses <a href="https://web.dev/file-system-access/">the File System Access API</a>
</div>


<script>
    const selectDirectoryElementId = "select-directory";
    const outputElementId = "output";

    const getFilesAndDirNodeForHandle = async (dirHandle) => {
        const node = {
            name: dirHandle.name,
            kind: dirHandle.kind,
            handle: dirHandle,
            children: [],
        };

        if (dirHandle.kind === "directory") {
            for await (const [_, handle] of dirHandle) {
                node.children.push(await getFilesAndDirNodeForHandle(handle));
            }
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
        const node = await getFilesAndDirNodeForHandle(dirHandle);
        console.log(node);

        const display = getStructureDisplay(node);
        const outputElement = document.getElementById(outputElementId);
        outputElement.innerText = display;
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
    });
</script>