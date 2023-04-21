import React, { useState, useEffect } from "react";
import {
    Typography,
    TextField,
    Button,
    Select,
    MenuItem,
    FormControl,
    InputLabel, ButtonGroup, Collapse,
} from "@material-ui/core";
import MaterialTable from 'material-table';
import { tableIcons } from "./Utils";
import { Alert } from "@material-ui/lab";

const ManageAccountsPage = () => {
  const [successMsg, setSuccessMsg] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [employeeType, setEmployeeType] = useState("");

  const [employees, setEmployees] = useState([]);
  const loadEmployees = () => {
    fetch('/api/get-all-employees')
      .then((response) => response.json())
      .then((data) => {
        setEmployees(data);
        console.log(data);
      });
  }
  useEffect(() => {
    loadEmployees();
  }, []);


  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleEmployeeTypeChange = (event) => {
    setEmployeeType(event.target.value);
  };

  const handleCreateAccount = () => {
    // TODO: implement create account functionality
  };

  const handleUpdateAccount = () => {
    // TODO: implement update account functionality
  };

  const handleDeleteAccount = () => {
    // TODO: implement delete account functionality
  };


  const [selectedRow, setSelectedRow] = useState(null);
  const getEmployeesTable = () => {
    const columns = [
        { title: 'ID', field: 'id' },
        { title: 'Username', field: 'username' },
        { title: 'Type', field: 'type' }
    ];

    return (
          <MaterialTable
              title='Employees'
              columns={columns}
              data={employees}
              icons={tableIcons}
              onRowClick={(evt, selectedRow) => {
                setSelectedRow(selectedRow);
              }}
              options={{
              rowStyle: (rowData) => ({
                backgroundColor:
                    selectedRow === rowData ? "#6ABAC9" : "#FFF",
                })
              }}
          />
    );
  }

  return (
      <div>
        <Typography variant="h4">
          Manage Accounts
        </Typography>

        <FormControl fullWidth margin='normal'>
          <InputLabel>Employee Type</InputLabel>
          <Select value={employeeType} onChange={handleEmployeeTypeChange} required>
            <MenuItem value="Administrator">Administrator</MenuItem>
            <MenuItem value="Tester">Tester</MenuItem>
            <MenuItem value="Programmer">Programmer</MenuItem>
          </Select>
          <TextField
              label='Username'
              value={username}
              onChange={handleUsernameChange}
          />
          <TextField
              label='Password'
              type="password"
              value={password}
              onChange={handlePasswordChange}
            />
        </FormControl>

        <ButtonGroup fullWidth style={{gap: 20}}>
          <Button variant="contained" color="primary" onClick={handleCreateAccount}>
            Create Account
          </Button>
          <Button variant="contained" color="primary" onClick={handleUpdateAccount}>
            Update Account
          </Button>
          <Button variant="contained" color="secondary" onClick={handleDeleteAccount}>
            Delete Account
          </Button>
        </ButtonGroup>

        <div>
          {getEmployeesTable()}
        </div>

      </div>
  );
};

export default ManageAccountsPage;