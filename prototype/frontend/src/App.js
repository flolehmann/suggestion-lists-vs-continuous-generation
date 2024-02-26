import React from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import { StartingPage } from './pages/StartingPage';
import { AgreementPage } from './pages/AgreementPage';
import { WritingPage } from './pages/WritingPage';
import { TaskPage } from './pages/TaskPage';
import { ResultPage } from './pages/ResultPage';
import { FinishPage } from './pages/FinishPage';

import './App.css';

//export const BACKEND_URL = process.env.BACKEND_URL || ""
export const BACKEND_URL = "YOUR BACKEND URL"

class App extends React.Component {
  
  // see "homepage" entry in package.json for the value of PUBLIC_URL. Maybe an .env file could be used for that?
  render() {
    return (
      <div className="App">
        <Router basename={process.env.PUBLIC_URL}>
          <Switch>
            <Route exact path="/"> <StartingPage/> </Route>
            <Route path="/version:version"> <WritingPage/> </Route>
            <Route path="/agreement"> <AgreementPage/> </Route>
            <Route exact path="/task:tid"> <TaskPage/> </Route>
            <Route path="/task:tid/writing"> <WritingPage/> </Route>
            <Route path="/task:tid/result"> <ResultPage/> </Route>
            <Route path="/finished"> <FinishPage/> </Route>
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;

export function to_string(arr) {
  let s = '';
  for (let w of arr) {
    s += w + ' '
  }
  return s.slice(0, -1) // To remove the last whitespace
}
