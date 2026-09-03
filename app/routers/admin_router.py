from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.db import engine, get_db


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)
@router.get("/tables")
def list_tables():
    inspector = inspect(engine)
    return inspector.get_table_names()


@router.get("/tables/{table_name}")
def get_table_data(
    table_name: str,
    db: Session = Depends(get_db),
):
    inspector = inspect(engine)

    tables = inspector.get_table_names()

    if table_name not in tables:
        raise HTTPException(
            status_code=404,
            detail="Table not found"
        )

    columns = [
        column["name"]
        for column in inspector.get_columns(table_name)
    ]

    result = db.execute(
        text(f'SELECT * FROM "{table_name}"')
    )

    rows = [
        dict(row._mapping)
        for row in result
    ]

    return {
        "columns": columns,
        "rows": rows,
    }
@router.get("", response_class=HTMLResponse)
def admin_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Enterprise AI Agent - Admin</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                background: #f5f5f5;
            }

            header {
                background: #222;
                color: white;
                padding: 16px 24px;
                font-size: 20px;
            }

            .container {
                display: flex;
                height: calc(100vh - 56px);
            }

            .sidebar {
                width: 220px;
                background: white;
                border-right: 1px solid #ddd;
                padding: 16px;
            }

            .table-item {
                padding: 10px;
                cursor: pointer;
                border-radius: 5px;
                margin-bottom: 4px;
            }

            .table-item:hover {
                background: #eee;
            }

            .table-item.active {
                background: #ddd;
                font-weight: bold;
            }

            .content {
                flex: 1;
                padding: 24px;
                overflow: auto;
            }

            .table-wrapper {
                overflow-x: auto;
                background: white;
            }

            table {
                border-collapse: collapse;
                width: 100%;
            }

            th,
            td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
                vertical-align: top;
            }

            th {
                background: #eee;
                position: sticky;
                top: 0;
                z-index: 2;
            }

            .column-header {
                cursor: pointer;
                user-select: none;
            }

            .column-header:hover {
                background: #ddd;
            }

            .filter-input {
                width: 95%;
                box-sizing: border-box;
                margin-top: 6px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }

            .sort-indicator {
                margin-left: 5px;
                font-size: 12px;
            }

            .empty {
                color: #777;
            }

            .row-count {
                margin-bottom: 12px;
                color: #666;
                font-size: 14px;
            }
        </style>
    </head>

    <body>

        <header>
            Enterprise AI Agent — Database Admin
        </header>

        <div class="container">

            <div class="sidebar">
                <h3>Tables</h3>
                <div id="tables"></div>
            </div>

            <div class="content">

                <h2 id="table-title">
                    Select a table
                </h2>

                <div id="table-data">
                    <p class="empty">
                        Select a table from the left.
                    </p>
                </div>

            </div>

        </div>

        <script>

            let currentData = null;

            let filters = {};

            let sortColumn = null;

            let sortDirection = "asc";


            async function loadTables() {

                const response = await fetch("/admin/tables");

                const tables = await response.json();

                const container = document.getElementById("tables");

                container.innerHTML = "";

                tables.forEach(table => {

                    const element = document.createElement("div");

                    element.className = "table-item";

                    element.innerText = table;

                    element.onclick = () => {

                        document
                            .querySelectorAll(".table-item")
                            .forEach(item => item.classList.remove("active"));

                        element.classList.add("active");

                        loadTable(table);
                    };

                    container.appendChild(element);

                });
            }


            async function loadTable(tableName) {

                document.getElementById("table-title").innerText =
                    tableName;

                const response =
                    await fetch(`/admin/tables/${tableName}`);

                currentData = await response.json();

                filters = {};

                sortColumn = null;

                sortDirection = "asc";

                renderTable();

            }


            function renderTable() {

                const container =
                    document.getElementById("table-data");

                if (!currentData || currentData.rows.length === 0) {

                    container.innerHTML =
                        "<p class='empty'>No records found.</p>";

                    return;
                }


                let rows = [...currentData.rows];


                // -------------------------
                // Apply filters
                // -------------------------

                rows = rows.filter(row => {

                    return currentData.columns.every(column => {

                        const filter =
                            filters[column];

                        if (!filter) {
                            return true;
                        }

                        let value = row[column];

                        if (value === null ||
                            value === undefined) {

                            value = "";

                        }

                        if (typeof value === "object") {

                            value = JSON.stringify(value);

                        }

                        return String(value)
                            .toLowerCase()
                            .includes(filter.toLowerCase());

                    });

                });


                // -------------------------
                // Apply sorting
                // -------------------------

                if (sortColumn !== null) {

                    rows.sort((a, b) => {

                        let valueA = a[sortColumn];

                        let valueB = b[sortColumn];


                        if (valueA === null ||
                            valueA === undefined) {

                            valueA = "";

                        }

                        if (valueB === null ||
                            valueB === undefined) {

                            valueB = "";

                        }


                        if (typeof valueA === "object") {
                            valueA = JSON.stringify(valueA);
                        }

                        if (typeof valueB === "object") {
                            valueB = JSON.stringify(valueB);
                        }


                        // Numeric sorting

                        const numberA = Number(valueA);

                        const numberB = Number(valueB);

                        if (!isNaN(numberA) &&
                            !isNaN(numberB) &&
                            valueA !== "" &&
                            valueB !== "") {

                            return sortDirection === "asc"
                                ? numberA - numberB
                                : numberB - numberA;
                        }


                        // String sorting

                        valueA = String(valueA).toLowerCase();

                        valueB = String(valueB).toLowerCase();


                        if (valueA < valueB) {
                            return sortDirection === "asc"
                                ? -1
                                : 1;
                        }

                        if (valueA > valueB) {
                            return sortDirection === "asc"
                                ? 1
                                : -1;
                        }

                        return 0;

                    });

                }


                let html = "";

                html += `
                    <div class="row-count">
                        Showing ${rows.length} of ${currentData.rows.length} rows
                    </div>
                `;


                html += "<div class='table-wrapper'>";

                html += "<table>";

                html += "<thead>";

                html += "<tr>";


                currentData.columns.forEach(column => {

                    let indicator = "";

                    if (sortColumn === column) {

                        indicator =
                            sortDirection === "asc"
                                ? "▲"
                                : "▼";

                    }


                    html += `

                        <th>

                            <div
                                class="column-header"
                                onclick="sortBy('${column}')"
                            >

                                ${column}

                                <span class="sort-indicator">
                                    ${indicator}
                                </span>

                            </div>

                            <input
                                class="filter-input"
                                placeholder="Filter..."
                                value="${filters[column] || ""}"
                                oninput="filterBy('${column}', this.value)"
                                onclick="event.stopPropagation()"
                            >

                        </th>

                    `;

                });


                html += "</tr>";

                html += "</thead>";

                html += "<tbody>";


                rows.forEach(row => {

                    html += "<tr>";


                    currentData.columns.forEach(column => {

                        let value = row[column];


                        if (value === null ||
                            value === undefined) {

                            value = "";

                        }


                        if (typeof value === "object") {

                            value =
                                JSON.stringify(value);

                        }


                        html += `
                            <td>${value}</td>
                        `;

                    });


                    html += "</tr>";

                });


                html += "</tbody>";

                html += "</table>";

                html += "</div>";


                container.innerHTML = html;

            }


            function sortBy(column) {

                if (sortColumn === column) {

                    sortDirection =
                        sortDirection === "asc"
                            ? "desc"
                            : "asc";

                } else {

                    sortColumn = column;

                    sortDirection = "asc";

                }

                renderTable();

            }


            function filterBy(column, value) {

                filters[column] = value;

                renderTable();

                // Restore focus to the filter input

                const inputs =
                    document.querySelectorAll(".filter-input");

                inputs.forEach(input => {

                    if (input.value === value) {
                        input.focus();
                    }

                });

            }


            loadTables();

        </script>

    </body>

    </html>
    """