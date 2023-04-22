import React, { useState, useEffect } from 'react';
import MaterialTable from "material-table";
import { renderStatus, tableIcons } from "./Utils";

export default function BugsListPage() {
    const [bugs, setBugs] = useState([]);
    const loadBugs = () => {
        fetch('/api/get-all-bugs')
            .then((response) => response.json())
            .then((data) => {
                setBugs(data);
            });
    }
    useEffect(() => {
        loadBugs();
    }, []);


    const [selectedRow, setSelectedRow] = useState(null);
    const getBugsTable = () => {
        const columns = [
            {title: 'ID', field: 'id', defaultSort: 'desc'},
            {title: 'Title', field: 'title'},
            {title: 'Description', field: 'description', hidden: true},
            {title: 'Status', field: 'status', render: rowData => renderStatus(rowData.status) },
            {title: 'Created at', field: 'created_at', hidden: true},
            {title: 'Reporter', field: 'reporter'},
            {title: 'Solver', field: 'solver'}
        ];

        return (
            <MaterialTable
                title='Bugs'
                columns={columns}
                data={bugs}
                icons={tableIcons}
                onRowClick={(evt, currentSelectedRow) => {
                    if (selectedRow === currentSelectedRow) {
                        setSelectedRow(null);
                        return;
                    }
                    console.log(currentSelectedRow);
                    setSelectedRow(currentSelectedRow);
                }}
                options={{
                    rowStyle: (rowData) => ({
                        backgroundColor: selectedRow === rowData ? "#5972FF" : "#FFF",
                    })
                }}
            />
        );
    }

    return (
      <>
        {getBugsTable()}
      </>
    );
}