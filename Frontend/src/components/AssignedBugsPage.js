import React, {useEffect, useState} from 'react';
import {renderStatus, tableIcons} from "./Utils";
import MaterialTable from "material-table";
import {Button, ButtonGroup, Collapse, FormControl, TextField, Typography} from "@material-ui/core";
import {Alert} from "@material-ui/lab";

export default function AssignedBugsPage() {
    const [successMsg, setSuccessMsg] = useState('');
    const [errorMsg, setErrorMsg] = useState('');

    const [bugs, setBugs] = useState([]);
    const loadBugs = () => {
        fetch('/api/get-programmer-bugs')
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
            {title: 'Description', field: 'description'},
            {title: 'Status', field: 'status', hidden: true },
            {title: 'Created at', field: 'created_at', hidden: true},
            {title: 'Reporter', field: 'reporter'},
            {title: 'Solver', field: 'solver', hidden: true}
        ];

        return (
            <MaterialTable
                title='Submitted Bugs'
                columns={columns}
                data={bugs}
                icons={tableIcons}
                onRowClick={(evt, currentSelectedRow) => {
                    if (selectedRow === currentSelectedRow) {
                        setSelectedRow(null);
                        return;
                    }
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

    const handleBugFixed = () => {
        // TODO: handle bug fixed
    }

    const handleBugUnassign = () => {
        // TODO: handle bug unassign
    }

    return ( <>
            <Typography variant="h4">
              Your Assignments
            </Typography>

            <ButtonGroup fullWidth className='gap-20'>
              <Button
                  variant='contained'
                  color='primary'
                  onClick={handleBugFixed}
                  disabled={selectedRow === null}>
                Mark Bug as Fixed
              </Button>
              <Button
                  variant='contained'
                  color='secondary'
                  onClick={handleBugUnassign}
                  disabled={selectedRow === null}
              >
                Mark Bug as Unassigned
              </Button>
            </ButtonGroup>

            <Collapse in={successMsg !== '' || errorMsg !== ''}>
                <Alert severity={successMsg !== '' ? 'success' : 'error'} onClose={ () => {
                    setErrorMsg('');
                    setSuccessMsg('');
                    }}>
                    {successMsg !== '' ? successMsg : errorMsg}
                </Alert>
            </Collapse>

            <div>
                {getBugsTable()}
            </div>
        </>
    );
}