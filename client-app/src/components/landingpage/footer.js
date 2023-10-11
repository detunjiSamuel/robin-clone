import React, { useEffect } from "react";

import "../../css/landingpageFooter.css";

import flaskIcon from "../../assets/flask.svg"
import amazonAWS from "../../assets/amazonaws.svg"
import css from "../../assets/css3.svg"
import html from "../../assets/html5.svg"
import javascript from "../../assets/javascript.svg"
import npm from "../../assets/npm.svg"
import postgres from "../../assets/postgresql.svg"
import python from "../../assets/python.svg"
import react from "../../assets/react.svg"
import reactRouter from "../../assets/reactrouter.svg"
import redux from "../../assets/redux.svg"
import render from "../../assets/render.svg"
import sqla from "../../assets/sqla.png"



function LandingFooter() {
 return (
     <div id="footer-container">
         <div id="footer-top-container">
             <div id="footer-top-left-container">
                 <div id="footer-top-left-content">
                     <div id="top-footer-text">Hosted by</div>
                     <div id="render-info">
                         <div id="icons" className="render-icon">
                             <img className="backend-icons" src={render} alt="render-icon" />
                             Render
                         </div>
                     </div>
                 </div>
             </div>
             <div id="footer-top-right-container">
                 <div id="footer-top-right-content">
                     <div id="top-footer-text">Made with</div>
                     <div id="icons">
                         <img className="made-with-icons" src={npm} alt="npm-icon" />
                         <img className="made-with-icons" src={python} alt="python-icon" />
                         <img className="made-with-icons" src={sqla} alt="sqla-icon" />
                         <img className="made-with-icons" src={flaskIcon} alt="flask-icon" />
                         <img className="made-with-icons" src={amazonAWS} alt="aws-icon" />
                         <img className="made-with-icons" src={css} alt="css-icon" />
                         <img className="made-with-icons" src={html} alt="html-icon" />
                         <img className="made-with-icons" src={javascript} alt="javascript-icon" />
                         <img className="made-with-icons" src={redux} alt="redux-icon" />
                         <img className="made-with-icons" src={react} alt="react-icon" />
                         <img className="made-with-icons" src={postgres} alt="postgresql-icon" />
                         <img className="made-with-icons" src={reactRouter} alt="react-icon" />
                     </div>
                 </div>
             </div>

         </div>
         <div id="footer-bottom-container">
             <div id="footer-bottom-left">
                 <div id="footer-bottom-left-content">
                     <div className="names" id="name-container">
                         Adetunji Samuel
                         <a href="https://github.com/detunjiSamuel">
                             Github
                         </a>
                         <a href="https://www.linkedin.com/in/samuel-adetunji-404249174">
                             LinkedIn
                         </a>
                     </div>

                 </div>
             </div>
             <div id="footer-bottom-right">
                 <div id="footer-bottom-right-content">
                     <div id="text-disclaimer">
                         <div id="disclaimer">
                             All investing involves risk. No deposit needed. Any money in used is virtual money.
                         </div>
                         <div id="disclaimer">
                             This site is not Robinhood. Please do not provide your personal information.we  will not be responsible for any trades made based off of this cloned site.
                         </div>
                         <div id="disclaimer">
                             © 2022. All rights reserved.

                         </div>



                     </div>
                 </div>
             </div>


         </div>

     </div>
 )

}

export default LandingFooter;
