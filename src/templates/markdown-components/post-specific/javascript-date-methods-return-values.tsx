import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";

interface IJavascriptDateMethodsReturnValues {}

const removeZZoneFromDateISOString = (date: Date) => {
  const iso = date.toISOString();
  return iso.substr(0, iso.length - 1);
};

const JavascriptDateMethodsReturnValues: React.FC<IJavascriptDateMethodsReturnValues> = ({}) => {
  const [date, setDate] = useState(new Date());
  const [datePickerValue, setDatePickerValue] = useState(removeZZoneFromDateISOString(new Date()));

  const dateFunctions = (Object.getOwnPropertyNames(Object.getPrototypeOf(new Date())) as Array<
    keyof Date
  >)
    .sort()
    .filter((f: string) => f !== "constructor" && !f.startsWith("set"));

  return (
    <>
      <h2>Target Date</h2>
      <div className="form-inline" style={{ justifyContent: "center" }}>
        <div className="form-group mr-sm-3 mb-2">
          <Form.Control
            type="datetime-local"
            value={datePickerValue}
            onChange={e => {
              setDatePickerValue(e.currentTarget.value);
              setDate(new Date(e.currentTarget.value));
            }}
          />
        </div>
        <Button variant="primary" onClick={() => setDate(new Date())}>
          Set to Now
        </Button>
      </div>

      <blockquote className="my-2">
        <p>Onblur events on this datetime input will update all values below.</p>
      </blockquote>
      <h2>
        Conversion Getters (<code className="language-text">to...</code> calls)
      </h2>
      <ul>
        {dateFunctions
          .filter(f => f.startsWith("to"))
          .map(f => (
            <FunctionValue key={f} functionName={f} value={(date as any)[f]()} />
          ))}
      </ul>
      <h2>
        Getters (<code className="language-text">get...</code> calls)
      </h2>
      <ul>
        {dateFunctions
          .filter(f => f.startsWith("get"))
          .map(f => (
            <FunctionValue key={f} functionName={f} value={(date as any)[f]()} />
          ))}
      </ul>
      <h2>
        Other Methods (not <code className="language-text">to</code> or{" "}
        <code className="language-text">get</code>)
      </h2>
      <ul>
        {dateFunctions
          .filter(f => !f.startsWith("to") && !f.startsWith("get"))
          .map(f => (
            <FunctionValue key={f} functionName={f} value={(date as any)[f]()} />
          ))}
      </ul>
    </>
  );
};

const FunctionValue: React.FC<{ functionName: string; value: any }> = ({ functionName, value }) => {
  return (
    <li>
      <a
        href={`https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/${functionName}`}
      >
        .{functionName}(){" "}
      </a>
      : <code>{value}</code>
    </li>
  );
};

export default JavascriptDateMethodsReturnValues;
