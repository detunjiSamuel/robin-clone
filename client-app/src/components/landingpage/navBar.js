
import React, { useEffect } from "react";

import { NavLink, useLocation,  Navigate  } from "react-router-dom";

import { useSelector } from "react-redux";


import '../../css/landingpageNavBar.css'


function LandingNavBar() {
 const location = useLocation();
 const current_url = location.pathname;

 const user = useSelector(state => state.auth.user);

 if (user) {
     return <Navigate  to='/app' replace={true} />;
 }

 return (
  <div className="landing-page-container">
            <div className={`landing-page ${current_url === "/" ? "landing-page-green" : "landing-page-white"}`}>
                <NavLink  to="/">
                    <div className="landing-page-logo">
                        <p className="landing-page-logo-text">Robinhood</p>
                        <i className="fa-solid fa-rocket"></i>
                    </div>
                </NavLink>
                <div className="landing-page-navlink-actions-container">
                    <ul className="landing-page-navlinks">
                        <NavLink to="/invest">
                            <li className="landing-page-navlink" id="landing-page-Invest-button">Invest</li>
                        </NavLink>
                        <NavLink to="/learn">
                            <li className="landing-page-navlink" id="landing-page-learn-button">Learn</li>
                        </NavLink>
                        <NavLink to="/cashcard">
                            <li className="landing-page-navlink" id="landing-page-CashCard-button">RocketCard</li>
                        </NavLink>
                        <a className="landing-page-navlink" href="https://github.com/detunjiSamuel/robin-clone" target="_blank" rel="noopener noreferrer">Repository</a>
                    </ul>
                    <div className="landing-page-actions">
                        <NavLink to="/login" >
                            <button id="landing-page-login">
                                Log in
                            </button>
                        </NavLink>
                        <NavLink to="/register" >
                            <button id="landing-page-signup">
                                Sign up
                            </button>
                        </NavLink>
                    </div>
                </div>
            </div >
        </div>
 );
}



export default LandingNavBar