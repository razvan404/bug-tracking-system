import React, { useState, useEffect } from 'react';
import MaterialTable from "material-table";
import { renderStatus, tableIcons } from "./Utils";
import {Button, Card, CardContent, Typography} from "@material-ui/core";

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
            {title: 'Solver', field: 'solver', render: rowData => rowData.solver === '' ? rowData.solver : 'Not assigned yet'}
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

    return (
      <>
        <Typography variant="h4">
            Bugs List
        </Typography>
        {getBugsTable()}
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
                              Title: {selectedRow.title}
                          </Typography>
                          <Typography variant='body2' component='p'>
                              Description: {selectedRow.description}
                          </Typography>
                          <Typography variant='body2' component='p'>
                              Status: {selectedRow.status}
                          </Typography>
                          <Typography variant='body2' component='p'>
                              Created at: {selectedRow.created_at}
                          </Typography>
                          <Typography variant='body2' component='p'>
                              Reporter: {selectedRow.reporter}
                          </Typography>
                          <Typography variant='body2' component='p'>
                              Solver: {selectedRow.solver === '' ? selectedRow.solver : 'Not assigned yet'}
                          </Typography>
                          <Button
                              variant={'contained'}
                              color={'primary'}
                              onClick={() => {
                                  return true;
                              }}
                              disabled={employeeType !== 'programmer' || selectedRow.status !== 'unassigned'}
                          >
                              Assign this bug
                          </Button>
                      </>
                  }
              </CardContent>
          </Card>
      </>
    );
}