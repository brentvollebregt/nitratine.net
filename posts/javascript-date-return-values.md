title: "JavaScript Date Return Values"
date: 2019-05-07
category: General
tags: [javascript tool]
feature: feature.png
description: "This is a tool to help you quickly look at function return types of a JavaScript date object and change the date to see what happens"

## Date
<div class="form-inline">
  <div class="form-group mr-sm-3 mb-2">
    <input type="datetime-local" class="form-control" id="dateInput">
  </div>
  <button type="submit" class="btn btn-primary mb-2" id="setDateToNow">Set to Now</button>
</div>

## String Methods
- toDateString()
- toISOString()
- toJSON()
- ...

## Get Methods
- getDate
- getDay
- getFullYear
- getHours
- getMilliseconds
- getMinuets
- getMonth
- getSeconds
- getTime
- getTimezoneOffset
- getUTCDate
- getUTCDay
- getUTCFullYear
- getUTCHours
- getUTCMilliseconds
- getUTCMinutes
- getUTCMonth
- getUTCSeconds
- getYear

<script>
    function adjustDateToMakeISOCurrentTimezone(date) {
        return new Date(date.getTime() - (date.getTimezoneOffset() * 60 * 1000));
    }
    
    function setDateToNow() {
        let date = new Date();
        let dAdjusted = adjustDateToMakeISOCurrentTimezone(date);
        setDate(dAdjusted);
    }
    
    function setDate(date) {
        let dateISO = date.toISOString();
        document.getElementById('dateInput').value = dateISO.substr(0, dateISO.length - 1);
    }
    
    // Event listeners
    document.getElementById('setDateToNow').addEventListener('click', setDateToNow);
    document.getElementById('dateInput').addEventListener('blur', function(e) {
        console.log(e.target.value);
        setDate(adjustDateToMakeISOCurrentTimezone(new Date(e.target.value)));
    });
    
    // Load
    setDateToNow();
</script>
