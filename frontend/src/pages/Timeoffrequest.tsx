import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Timeoffrequest: React.FC = () => {
  return (
    <div id="page-timeoffrequest-2">
    <div id="iacwl" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="iz8ho" style={{
          "width": "250px",
          "padding": "20px",
          "display": "flex",
          "overflowY": "auto",
          "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)",
          "color": "white",
          "--chart-color-palette": "default",
          "flexDirection": "column"
        }}>
        <h2 id="iqt0z" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="iqtlu" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="ivn07" style={{
              "padding": "10px 15px",
              "textDecoration": "none",
              "marginBottom": "5px",
              "display": "block",
              "background": "transparent",
              "color": "white",
              "borderRadius": "4px",
              "--chart-color-palette": "default"
            }} href="/employee">{"Employee"}</a>
          <a id="it2ge" style={{
              "padding": "10px 15px",
              "textDecoration": "none",
              "marginBottom": "5px",
              "display": "block",
              "background": "transparent",
              "color": "white",
              "borderRadius": "4px",
              "--chart-color-palette": "default"
            }} href="/manager">{"Manager"}</a>
          <a id="i7lpk" style={{
              "padding": "10px 15px",
              "textDecoration": "none",
              "marginBottom": "5px",
              "display": "block",
              "background": "rgba(255,255,255,0.2)",
              "color": "white",
              "borderRadius": "4px",
              "--chart-color-palette": "default"
            }} href="/timeoffrequest">{"TimeOffRequest"}</a>
        </div>
        <p id="id9tk" style={{
            "fontSize": "11px",
            "paddingTop": "20px",
            "marginTop": "auto",
            "textAlign": "center",
            "opacity": "0.8",
            "borderTop": "1px solid rgba(255,255,255,0.2)",
            "--chart-color-palette": "default"
          }}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="iiz7j" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="id4fz" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"TimeOffRequest"}</h1>
        <p id="i4wca" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage TimeOffRequest data"}</p>
        <TableBlock id="table-timeoffrequest-2" className="has-data-binding" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="TimeOffRequest List" options={{
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
                "label": "StartDate",
                "column_type": "field",
                "field": "startDate",
                "type": "date",
                "required": true
              },
              {
                "label": "EndDate",
                "column_type": "field",
                "field": "endDate",
                "type": "date",
                "required": true
              },
              {
                "label": "Reason",
                "column_type": "field",
                "field": "reason",
                "type": "str",
                "required": true
              },
              {
                "label": "SubmittedAt",
                "column_type": "field",
                "field": "submittedAt",
                "type": "datetime",
                "required": true
              },
              {
                "label": "ApprovedAt",
                "column_type": "field",
                "field": "approvedAt",
                "type": "datetime",
                "required": true
              },
              {
                "label": "Status",
                "column_type": "field",
                "field": "status",
                "type": "enum",
                "options": [
                  "APPROVED",
                  "CANCELLED",
                  "PENDING",
                  "REJECTED"
                ],
                "required": true
              },
              {
                "label": "Requester",
                "column_type": "lookup",
                "path": "requester",
                "entity": "Employee",
                "field": "name",
                "type": "str",
                "required": true
              },
              {
                "label": "ApprovedBy",
                "column_type": "lookup",
                "path": "approvedBy",
                "entity": "Manager",
                "field": "name",
                "type": "str",
                "required": false
              }
            ],
            "formColumns": [
              {
                "column_type": "field",
                "field": "startDate",
                "label": "startDate",
                "type": "date",
                "required": true,
                "defaultValue": null
              },
              {
                "column_type": "field",
                "field": "endDate",
                "label": "endDate",
                "type": "date",
                "required": true,
                "defaultValue": null
              },
              {
                "column_type": "field",
                "field": "reason",
                "label": "reason",
                "type": "str",
                "required": true,
                "defaultValue": null
              },
              {
                "column_type": "field",
                "field": "submittedAt",
                "label": "submittedAt",
                "type": "datetime",
                "required": true,
                "defaultValue": null
              },
              {
                "column_type": "field",
                "field": "approvedAt",
                "label": "approvedAt",
                "type": "datetime",
                "required": false,
                "defaultValue": null
              },
              {
                "column_type": "field",
                "field": "status",
                "label": "status",
                "type": "enum",
                "required": true,
                "defaultValue": null,
                "options": [
                  "APPROVED",
                  "CANCELLED",
                  "PENDING",
                  "REJECTED"
                ]
              },
              {
                "column_type": "lookup",
                "path": "requester",
                "field": "requester",
                "lookup_field": "name",
                "target_field": "id",
                "target_type": "int",
                "entity": "Employee",
                "type": "str",
                "required": true
              },
              {
                "column_type": "lookup",
                "path": "approvedBy",
                "field": "approvedBy",
                "lookup_field": "name",
                "target_field": "id",
                "target_type": "int",
                "entity": "Manager",
                "type": "str",
                "required": false
              }
            ]
          }} dataBinding={{"entity": "TimeOffRequest", "endpoint": "/timeoffrequest/", "row_key_fields": ["id"]}} />
      </main>
    </div>    </div>
  );
};

export default Timeoffrequest;
