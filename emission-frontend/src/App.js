import { Routes, Route, BrowserRouter as Router } from 'react-router-dom';

import HeaderBar from "./HeaderBar/HeaderBar";
import EmissionsPage from "./EmissionSummaryPage/EmissionSummaryPage";
import UserInfoInput from './Register/Register';
import UserLoginInput from './Login/Login';
import LogOut from './Logout/Logout';

function App() {
  return (
    <Router>
      <HeaderBar />
      <Routes>
        <Route exact path="/register" element={<UserInfoInput/>}>
        </Route>
        <Route exact path="/login" element={<UserLoginInput/>}>
        </Route>
        <Route exact path="/logout" element={<LogOut/>}>
        </Route>
        <Route exact path="/" element={<EmissionsPage/>}>
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
