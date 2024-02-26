import { Outlet, useLocation } from "react-router-dom";
import React from "react";
import Navbar from "./navbar/navbar";

const Layout = () => {
    const location = useLocation();
    const { pathname } = location;

    const isLoginPage = pathname === '/';
    const isRegisterPage = pathname === '/register';

    // Determine whether to show the navbar based on the route
    const showNavbar = !isLoginPage && !isRegisterPage;

    return(
        <div>
            {showNavbar && <Navbar />}
            <Outlet/>
        </div>
    )
}

export default Layout;
