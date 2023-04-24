import React, { useState, useEffect } from 'react';
import MaterialTable from "material-table";
import { renderStatus, tableIcons } from "./Utils";
import { Button, Card, CardContent, Collapse, Typography } from "@material-ui/core";
import { Alert } from "@material-ui/lab";

export default function BugsListPage() {
    const [bugs, setBugs] = useState([]);
    const [employeeType, setEmployeeType] = useState('');

    useEffect( () => {
        (async () => {
          await fetch('/api/get-employee')
            .then((response) => {
              return response.json();
            })
            .then((data) => {
              setEmployeeType(data.type);
            });
        })();
      }, []);

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


    const [successMsg, setSuccessMsg] = useState('');
    const [errorMsg, setErrorMsg] = useState('');

    const handleAssignBug = () => {
        fetch('/api/assign-bug', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: selectedRow.id
            })
        })
            .then((response) => {
                if (response.ok) {
                    response.json().then((data) => setSuccessMsg(data.msg));
                    loadBugs();
                } else {
                    response.json().then((data) => setErrorMsg(data.error));
                }
            });
    }

    return (
      <>
        <Typography variant="h4">
            Bugs List
        </Typography>
        {getBugsTable()}
          <Collapse in={successMsg !== '' || errorMsg !== ''}>
             <Alert severity={successMsg !== '' ? 'success' : 'error'} onClose={ () => {
                setErrorMsg('');
                setSuccessMsg('');
                }}>
                {successMsg !== '' ? successMsg : errorMsg}
            </Alert>
          </Collapse>
        <Collapse in={selectedRow !== null}>
          <Card align='center'>
              <CardContent>
                  <Typography variant='h5' component='h5'>
                      Selected bug
                  </Typography>
                  {selectedRow === null
                      ? <Typography variant='body2' component='p'>
                          No bug selected
                  </Typography>
                      : <>
                          <Typography variant='body1' component='p'>
                              Title: {selectedRow['title']}
                          </Typography>
                          <Typography variant='body2' component='p'>
                              Description: {selectedRow['description']}
                          </Typography>
                          <Typography variant='body2' component='p'>
                              Status: {selectedRow['status']}
                          </Typography>
                          <Typography variant='body2' component='p'>
                              Created at: {selectedRow['created_at']}
                          </Typography>
                          <Typography variant='body2' component='p'>
                              Reporter: {selectedRow['reporter']}
                          </Typography>
                          {selectedRow.solver !== null
                              ? <Typography variant='body2' component='p'>Solver: {selectedRow.solver}</Typography>
                              : null}
                          <Button
                              variant={'contained'}
                              color={'primary'}
                              onClick={handleAssignBug}
                              disabled={employeeType !== 'programmer' || selectedRow.status !== 'unassigned'}
                          >
                              Assign this bug
                          </Button>
                      </>
                  }
              </CardContent>
          </Card>
        </Collapse>
      </>
    );
}