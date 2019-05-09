title: "JavaScript Date Methods Return Values"
date: 2019-05-08
category: General
tags: [javascript, tool]
feature: feature.png
description: "This is a tool to help you quickly look at function return types of a JavaScript date object and change the date to see what happens"

## Target Date
<div class="form-inline" style="justify-content: center;">
  <div class="form-group mr-sm-3 mb-2">
    <input type="datetime-local" class="form-control" id="dateInput">
  </div>
  <button type="submit" class="btn btn-primary mb-2" id="setDateToNow">Set to Now</button>
</div>

> Onblur events on this datetime input will update all values below.

## Conversion Getters (`to...` calls)
<ul id="jsDateFunctionsTo"></ul>

## Getters (`get...` calls)
<ul id="jsDateFunctionsGet"></ul>

## Other Methods (not `to` or `get`)
<ul id="jsDateFunctionsOther"></ul>

<script>
    function adjustDateToMakeISOCurrentTimezone(date) {
        return new Date(date.getTime() - (date.getTimezoneOffset() * 60 * 1000));
    }
    
    function setDate(date) {
        let dateAdjusted = adjustDateToMakeISOCurrentTimezone(date);
        let dateAdjustedISO = dateAdjusted.toISOString();
        document.getElementById('dateInput').value = dateAdjustedISO.substr(0, dateAdjustedISO.length - 1);
        
        // Set all fields using `date`
        let functions = Object.getOwnPropertyNames(Object.getPrototypeOf(date)).sort().filter(f => f !== 'constructor' && !f.startsWith('set'));
        functions.forEach(f => {
            console.log('testing', f);
            let valueNode = document.getElementById('jsDateFunction' + f);
            valueNode.textContent = date[f]();
        });
    }
    
    function setupPage() {
        // TODO Intially setup nodes and give everything id's. Don't display constructor and any set... methods.
        let date = new Date();
        let functions = Object.getOwnPropertyNames(Object.getPrototypeOf(date)).sort().filter(f => f !== 'constructor' && !f.startsWith('set'));
        
        let jsDateFunctionsTo = document.getElementById('jsDateFunctionsTo');
        let jsDateFunctionsGet = document.getElementById('jsDateFunctionsGet');
        let jsDateFunctionsOther = document.getElementById('jsDateFunctionsOther');
        
        functions.forEach(f => {
            let functionIdOnPage = 'jsDateFunction' + f;
            if (f.startsWith('to')) {
                addNode(jsDateFunctionsTo, functionIdOnPage, f);
            } else if (f.startsWith('get')) {
                addNode(jsDateFunctionsGet, functionIdOnPage, f);
            } else {
                addNode(jsDateFunctionsOther, functionIdOnPage, f);
            }
        });
    }
    
    function addNode(parent, id, functionName) {
        let li = document.createElement('li');
        let functionText = document.createElement('a');
        let textSpace = document.createTextNode(' : ');
        let value = document.createElement('code');
        functionText.textContent = '.' + functionName + '()';
        functionText.href = 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/' + functionName;
        value.id = id;
        li.appendChild(functionText);
        li.appendChild(textSpace);
        li.appendChild(value);
        parent.appendChild(li);
    }
    
    // Event listeners
    document.getElementById('setDateToNow').addEventListener('click', function() {
        setDate(new Date());            
    });
    document.getElementById('dateInput').addEventListener('blur', function(e) {
        setDate(new Date(e.target.value));
    });
    
    // Setup everything on DOM load
    document.addEventListener("DOMContentLoaded", function(){
        setupPage();
        setDate(new Date());
    });
</script>
