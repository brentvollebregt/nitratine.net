title: "C# Class to Record Converter"
date: 2023-03-06
category: Tools
tags: [tool, c-sharp]
feature: feature.png
description: "This is a tool that helps convert a C# class into a C# record. It supports typical public get/set properties as well as property summaries."

Paste your C# class below and click the button to convert it to a C# record.

This tool supports typical public get/set properties as well as property summaries. It will safely ignore attributes, a constructor, and any other code that is not a public get/set property.

<div id="tool" class="mb-2">
    <textarea class="form-control" id="input" placeholder="Input C# class" rows="8"></textarea>
    <textarea class="form-control mt-2" id="output" placeholder="Output C# record will appear here" rows="4" readonly></textarea>
    <button type="button" class="btn btn-primary mt-1" id="copy-output-button">Copy Output</button>
</div>

<script>
    const inputElement = document.getElementById("input");
    const outputElement = document.getElementById("output");
    const copyOutputButton = document.getElementById("copy-output-button");

    const escapeRegExp = (text) => text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&'); // https://stackoverflow.com/a/9310752

    const convert = (input) => {
        if (input.trim() === "") {
            return "";
        }

        try {
            // Parse the class name
            const className = input.match(/\w+\s+class\s+(\w+)/)[1];

            // Parse all class properties and their associated summaries (if exists)
            const properties = input.match(/public\s+\S+\s+(\w+)\s*\{ get; set; \}/g).map((property) => {
                const name = property.match(/public\s+\S+\s+(\w+)\s*\{/)[1];
                const type = property.match(/public\s+(\S+)\s+\w+\s*\{/)[1];
                const summary = input.match(new RegExp(`<summary>([^<]+)<\\/summary>\\s+${escapeRegExp(property)}`))?.[1].trim().replace(/^\/+|\/+$/g, '').trim();
                return { name, type, summary };
            });

            // Build the docstring
            let docstring = properties.filter(p => p.summary !== undefined).map((property) => `/// <param name="${property.name}">${property.summary}</param>`).join('\n');
            docstring = docstring === "" ? "" : `${docstring}\n`;

            // Rebuild the class as a C# record
            const output = `${docstring}public record ${className}(${properties.map((property) => `${property.type} ${property.name}`).join(', ')});`;

            return output;
        } catch (e) {
            return "Error: Unable to parse input";
        }
    }

    inputElement.addEventListener("input", () => {
        outputElement.value = convert(inputElement.value);
    });
    copyOutputButton.addEventListener("click", () => {
        outputElement.select();
        outputElement.setSelectionRange(0, outputElement.value.length);
        document.execCommand("copy");
    });
</script>

## Example Input

This shows the basics of what can be entered - yours will most likely look a lot cleaner but it demonstrates the basics.

```csharp
public class Car
{
    public Car(int id, string name, string color, bool isManual)
    {
        Id = id;
        Name = name;
        Color = color;
        IsManual = isManual;
    }

    /// <summary>
    /// The id of the car
    /// </summary>
    [Required]
    public int Id { get; set; }

    /// <summary>
    /// The name given to the car
    /// </summary>
    public string Name { get; set; }

    public string Color { get; set; }

    [Required]
    /// <summary>
    /// Whether this car is a manual or not
    /// </summary>
    public bool IsManual { get; set; }
}
```
