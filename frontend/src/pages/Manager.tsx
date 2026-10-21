import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Manager: React.FC = () => {
  return (
    <div id="page-manager-1">
    <div id="i1uuh" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="isohg" style={{
          "width": "250px",
          "padding": "20px",
          "display": "flex",
          "overflowY": "auto",
          "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)",
          "color": "white",
          "--chart-color-palette": "default",
          "flexDirection": "column"
        }}>
        <h2 id="i0ohj" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="iiohk" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="iez01" style={{
              "padding": "10px 15px",
              "textDecoration": "none",
              "marginBottom": "5px",
              "display": "block",
              "background": "transparent",
              "color": "white",
              "borderRadius": "4px",
              "--chart-color-palette": "default"
            }} href="/employee">{"Employee"}</a>
          <a id="i371y" style={{
              "padding": "10px 15px",
              "textDecoration": "none",
              "marginBottom": "5px",
              "display": "block",
              "background": "rgba(255,255,255,0.2)",
              "color": "white",
              "borderRadius": "4px",
              "--chart-color-palette": "default"
            }} href="/manager">{"Manager"}</a>
          <a id="ib2dh" style={{
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
        <p id="i5uvv" style={{
            "fontSize": "11px",
            "paddingTop": "20px",
            "marginTop": "auto",
            "textAlign": "center",
            "opacity": "0.8",
            "borderTop": "1px solid rgba(255,255,255,0.2)",
            "--chart-color-palette": "default"
          }}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="iszbi" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="i8lvb" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"Manager"}</h1>
        <p id="imtce" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage Manager data"}</p>
        <TableBlock id="table-manager-1" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Manager List" options={{
            "showHeader": true,
            "stripedRows": false,
            "showPagination": true,
            "rowsPerPage": 5,
            "actionButtons": true,
            "columns": [
              {
                "label": "Department",
                "column_type": "field",
                "field": "department",
                "type": "str",
                "required": true
              },
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
                "label": "TeamMembers",
                "column_type": "lookup",
                "path": "teamMembers",
                "entity": "Employee",
                "field": "name",
                "type": "list",
                "required": false
              },
              {
                "label": "ApprovedRequests",
                "column_type": "lookup",
                "path": "approvedRequests",
                "entity": "TimeOffRequest",
                "field": "reason",
                "type": "list",
                "required": false
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
                "column_type": "field",
                "field": "department",
                "label": "department",
                "type": "str",
                "required": true,
                "defaultValue": null
              },
              {
                "column_type": "lookup",
                "path": "teamMembers",
                "field": "teamMembers",
                "lookup_field": "name",
                "target_field": "id",
                "target_type": "int",
                "entity": "Employee",
                "type": "list",
                "required": false
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
              },
              {
                "column_type": "lookup",
                "path": "approvedRequests",
                "field": "approvedRequests",
                "lookup_field": "reason",
                "target_field": "id",
                "target_type": "int",
                "entity": "TimeOffRequest",
                "type": "list",
                "required": false
              }
            ]
          }} dataBinding={{"entity": "Manager", "endpoint": "/manager/", "row_key_fields": ["id"]}} />
        <div id="iegnw" style={{"marginTop": "20px", "display": "flex", "--chart-color-palette": "default", "flexWrap": "wrap", "gap": "10px"}}>
          <MethodButton id="ivu5p" className="action-button-component" style={{
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
            }} endpoint="/manager/{manager_id}/methods/approveTimeOff/" label="approveTimeOff" parameters={[{"name": "request", "type": "TimeOffRequest", "required": true, "inputKind": "lookup", "entity": "TimeOffRequest", "lookupField": "id"}]} isInstanceMethod={true} instanceSourceTableId="table-manager-1" />
        </div>
      </main>
    </div>    </div>
  );
};

export default Manager;
