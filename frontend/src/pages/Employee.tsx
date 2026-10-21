import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Employee: React.FC = () => {
  return (
    <div id="page-employee-0">
    <div id="iy6o8" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="iriwh" style={{
          "width": "250px",
          "padding": "20px",
          "display": "flex",
          "overflowY": "auto",
          "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)",
          "color": "white",
          "--chart-color-palette": "default",
          "flexDirection": "column"
        }}>
        <h2 id="in9dd" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="iro9l" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="iuj7j" style={{
              "padding": "10px 15px",
              "textDecoration": "none",
              "marginBottom": "5px",
              "display": "block",
              "background": "rgba(255,255,255,0.2)",
              "color": "white",
              "borderRadius": "4px",
              "--chart-color-palette": "default"
            }} href="/employee">{"Employee"}</a>
          <a id="i5qv5" style={{
              "padding": "10px 15px",
              "textDecoration": "none",
              "marginBottom": "5px",
              "display": "block",
              "background": "transparent",
              "color": "white",
              "borderRadius": "4px",
              "--chart-color-palette": "default"
            }} href="/manager">{"Manager"}</a>
          <a id="i91sg" style={{
              "padding": "10px 15px",
              "textDecoration": "none",
              "marginBottom": "5px",
              "display": "block",
              "background": "transparent",
              "color": "white",
              "borderRadius": "4px",
              "--chart-color-palette": "default"
            }} href="/timeoffrequest">{"TimeOffRequest"}</a>
        </div>
        <p id="izilf" style={{
            "fontSize": "11px",
            "paddingTop": "20px",
            "marginTop": "auto",
            "textAlign": "center",
            "opacity": "0.8",
            "borderTop": "1px solid rgba(255,255,255,0.2)",
            "--chart-color-palette": "default"
          }}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="inu2z" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="ixhis" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"Employee"}</h1>
        <p id="ie5ry" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage Employee data"}</p>
        <TableBlock id="table-employee-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Employee List" options={{
            "showHeader": true,
            "stripedRows": false,
            "showPagination": true,
            "rowsPerPage": 5,
            "actionButtons": true,
            "columns": [
              {
                "label": "Id",
                "column_type": "field",
                "field": "id",
                "type": "int",
                "required": true
              },
              {
                "label": "Name",
                "column_type": "field",
                "field": "name",
                "type": "str",
                "required": true
              },
              {
                "label": "Email",
                "column_type": "field",
                "field": "email",
                "type": "str",
                "required": true
              },
              {
                "label": "HiredDate",
                "column_type": "field",
                "field": "hiredDate",
                "type": "date",
                "required": true
              },
              {
                "label": "Position",
                "column_type": "field",
                "field": "position",
                "type": "str",
                "required": true
              },
              {
                "label": "Manager",
                "column_type": "lookup",
                "path": "manager",
                "entity": "Manager",
                "field": "name",
                "type": "str",
                "required": false
              },
              {
                "label": "TimeOffRequests",
                "column_type": "lookup",
                "path": "timeOffRequests",
                "entity": "TimeOffRequest",
                "field": "reason",
                "type": "list",
                "required": false
              }
            ],
            "formColumns": [
              {
                "column_type": "field",
                "field": "name",
                "label": "name",
                "type": "str",
                "required": true,
                "defaultValue": null
              },
              {
                "column_type": "field",
                "field": "email",
                "label": "email",
                "type": "str",
                "required": true,
                "defaultValue": null
              },
              {
                "column_type": "field",
                "field": "hiredDate",
                "label": "hiredDate",
                "type": "date",
                "required": true,
                "defaultValue": null
              },
              {
                "column_type": "field",
                "field": "position",
                "label": "position",
                "type": "str",
                "required": true,
                "defaultValue": null
              },
              {
                "column_type": "lookup",
                "path": "manager",
                "field": "manager",
                "lookup_field": "name",
                "target_field": "id",
                "target_type": "int",
                "entity": "Manager",
                "type": "str",
                "required": false
              },
              {
                "column_type": "lookup",
                "path": "timeOffRequests",
                "field": "timeOffRequests",
                "lookup_field": "reason",
                "target_field": "id",
                "target_type": "int",
                "entity": "TimeOffRequest",
                "type": "list",
                "required": false
              }
            ]
          }} dataBinding={{"entity": "Employee", "endpoint": "/employee/", "row_key_fields": ["id"]}} />
        <div id="i8jn5" style={{"marginTop": "20px", "display": "flex", "--chart-color-palette": "default", "flexWrap": "wrap", "gap": "10px"}}>
          <MethodButton id="i1rcs" className="action-button-component" style={{
              "padding": "6px 14px",
              "fontSize": "13px",
              "fontWeight": "600",
              "textDecoration": "none",
              "letterSpacing": "0.01em",
              "display": "flex",
              "cursor": "pointer",
              "transition": "background 0.2s",
              "background": "linear-gradient(90deg, #2563eb 0%, #1e40af 100%)",
              "color": "#fff",
              "borderRadius": "4px",
              "border": "none",
              "boxShadow": "0 1px 4px rgba(37,99,235,0.10)",
              "--chart-color-palette": "default",
              "alignItems": "center"
            }} endpoint="/employee/{employee_id}/methods/askForTimeOff/" label="askForTimeOff" parameters={[
              {
                "name": "startDate",
                "type": "date",
                "required": true
              },
              {
                "name": "endDate",
                "type": "date",
                "required": true
              },
              {
                "name": "reason",
                "type": "str",
                "required": true
              }
            ]} isInstanceMethod={true} instanceSourceTableId="table-employee-0" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Employee;
