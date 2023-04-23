import React, { useState, useEffect } from 'react';
import { AppBar, Toolbar, Typography, Drawer, List, ListItem, ListItemIcon, ListItemText } from '@material-ui/core';
import { Dashboard, Settings, Help, ExitToApp } from '@material-ui/icons';
import { useNavigate } from 'react-router-dom';
import ManageAccountsPage from './ManageAccountsPage';
import BugsListPage from "./BugsListPage";
import SubmittedBugsPage from "./SubmittedBugsPage";

function MainPage() {
  const navigate = useNavigate();
  const [employee, setEmployee] = useState(null);

  useEffect( () => {
    (async () => {
      await fetch('/api/get-employee')
        .then((response) => {
          if (!response.ok) {
            navigate('/login', {replace: true});
          }
          return response.json();
        })
        .then((data) => {
          setEmployee(data);
        });
    })();
  }, []);

  const handleLogout = () => {
    fetch('/api/logout-employee', { method: 'DELETE' })
      .then((response) => {
        if (response.ok) {
          navigate('/login', {replace: true});
        }
      });
  }

  const [mainComponent, setMainComponent] = useState(<BugsListPage />);

  return (
    <div className='mainRoot'>
      <AppBar className='mainAppBar'>
        <Toolbar className='flex-container unselectable'>
          <Typography variant='h6' className='occupy-space' unselectable='on'>
            Bug Tracking System
          </Typography>
            {employee ?
                <Typography variant='body1' unselectable='on'>
                    logged as <strong>{ employee['username'] }</strong>
                </Typography> : null
            }
        </Toolbar>
      </AppBar>
      <Drawer
        className='mainDrawer'
        variant='permanent'
        classes={{
          paper: 'drawerPaper'
        }}
      >
        <Toolbar />
        <div className='mainDrawerContainer'>
          <List>
            <ListItem button>
              <ListItemIcon>
                <Dashboard />
              </ListItemIcon>
              <ListItemText primary='Bugs List' onClick={() => setMainComponent(<BugsListPage />)} />
            </ListItem>
            {employee && employee['type'] === 'administrator' ?
                <ListItem button>
                  <ListItemIcon>
                    <Settings />
                  </ListItemIcon>
                  <ListItemText primary='Manage Accounts' onClick={() => setMainComponent(<ManageAccountsPage />)} />
                </ListItem> : null
            }
            {employee && employee['type'] === 'tester' ?
                <ListItem button>
                  <ListItemIcon>
                    <Help />
                  </ListItemIcon>
                  <ListItemText primary='Submitted Bugs' onClick={() => setMainComponent(<SubmittedBugsPage />)} />
                </ListItem> : null
            }
            {employee && employee['type'] === 'programmer' ?
                <ListItem button>
                  <ListItemIcon>
                    <Help />
                  </ListItemIcon>
                  <ListItemText primary='Your Tasks' />
                </ListItem> : null
            }
          </List>
          <List>
            <ListItem button onClick={handleLogout}>
              <ListItemIcon>
                <ExitToApp />
              </ListItemIcon>
              <ListItemText primary='Logout' />
            </ListItem>
          </List>
        </div>
      </Drawer>
      <main className='mainContent'>
        <Toolbar />
          {mainComponent}
      </main>
    </div>
  );
}

export default MainPage;