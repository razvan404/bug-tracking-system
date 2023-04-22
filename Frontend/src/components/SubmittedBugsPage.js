import React, {useEffect, useState} from 'react';
import {renderStatus, tableIcons} from "./Utils";
import MaterialTable from "material-table";
import {
    Button,
    ButtonGroup,
    Collapse,
    FormControl,
    InputLabel,
    MenuItem,
    Select,
    TextField,
    Typography,
} from "@material-ui/core";
import {Alert} from "@material-ui/lab";

export default function SubmittedBugsPage() {
    const [title, setTitle] = useState('');
    const [titleError, setTitleError] = useState('');
    const [description, setDescription] = useState('');
    const [descriptionError, setDescriptionError] = useState('');

    const [successMsg, setSuccessMsg] = useState('');
    const [errorMsg, setErrorMsg] = useState('');

    const [bugs, setBugs] = useState([]);
    const loadBugs = () => {
        fetch('/api/get-tester-bugs')
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
            {title: 'Status', field: 'status', render: rowData => renderStatus(rowData.status) },
            {title: 'Created at', field: 'created_at', hidden: true},
            {title: 'Reporter', field: 'reporter', hidden: true},
            {title: 'Solver', field: 'solver', render: rowData => rowData.solver === '' ? rowData.solver : 'Not assigned yet'}
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
                        setTitle('');
                        setDescription('');
                        return;
                    }
                    setSelectedRow(currentSelectedRow);
                    setTitle(currentSelectedRow.title);
                    setDescription(currentSelectedRow.description);
                }}
                options={{
                    rowStyle: (rowData) => ({
                        backgroundColor: selectedRow === rowData ? "#5972FF" : "#FFF",
                    })
            }}
            />
        );
    }

    const validateInput = () => {
        let isValid = true;
        if (title.length < 3 || title.length > 32) {
            setTitleError('Title must be between 3 and 32 characters');
            isValid = false;
        }
        if (description.length < 3 || description.length > 256) {
            setDescriptionError('Description must be between 3 and 256 characters');
            isValid = false;
        }
        return isValid;
    }

    const handleBugReport = () => {
        // TODO: handle bug report
    }

    const handleBugUpdate = () => {
        // TODO: handle bug update
    }

    const handleBugRemove = () => {
        // TODO: handle bug remove
    }

    return ( <>
            <Typography variant="h4">
              Submitted Bugs
            </Typography>

            <FormControl fullWidth margin='normal'>
              <TextField
                  label='Title'
                  value={title}
                  onChange={(ev) => {setTitle(ev.target.value)}}
                  error={titleError !== ''}
                  helperText={titleError}
              />
              <TextField
                  label='Description'
                  value={description}
                  onChange={(ev) => {setDescription(ev.target.value)}}
                  error={descriptionError !== ''}
                  helperText={descriptionError}
                  multiline
                  maxRows={4}
              />
            </FormControl>

            <ButtonGroup fullWidth style={{gap: 20}}>
              <Button
                  variant="contained"
                  color="primary"
                  onClick={handleBugReport}>
                Report Bug
              </Button>
              <Button
                  variant="contained"
                  color="primary"
                  onClick={handleBugUpdate}
                  disabled={selectedRow === null || selectedRow.status !== 'unassigned'}
              >
                Update Bug
              </Button>
              <Button
                  variant="contained"
                  color="secondary"
                  onClick={handleBugRemove}
                  disabled={selectedRow === null || selectedRow.status !== 'unassigned'}>
                Remove Bug
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