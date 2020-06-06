import React from "react";
import { Container, Nav, Navbar } from "react-bootstrap";
import { Link } from "gatsby";
import { Location } from "@reach/router";
import navigationConfig from "../../config/navigation.json";

// const navbarLinks = [
//   {
//     path: "/",
//     title: "Home"
//   },
//   {
//     path: "/blog/",
//     title: "Blog"
//   },
//   {
//     path: "https://www.youtube.com/c/PyTutorials",
//     title: "YouTube"
//   },
//   {
//     path: "https://github.com/brentvollebregt",
//     title: "GitHub"
//   },
//   {
//     path: "/about/",
//     title: "About"
//   }
// ];

interface NavBarLinks {
  title: string;
  path: string;
}

const Navigation = () => {
  const navbarLinks: NavBarLinks[] = navigationConfig.links;

  return (
    <Navbar collapseOnSelect expand="md" bg="dark" variant="dark" sticky="top">
      <Container>
        <Navbar.Brand>
          <img
            src="/assets/logo.png"
            height="30"
            className="d-inline-block align-top"
            alt="Nitratine Logo"
            style={{ cursor: "pointer" }}
          />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="mr-auto">
            {navbarLinks.map(({ path, title }) => (
              <Location key={path}>
                {locationProps => (
                  <Nav.Link
                    key={path}
                    href={path}
                    as={
                      path.startsWith("http://") || path.startsWith("https://") ? undefined : Link
                    }
                    to={path} // to is for Link
                    active={locationProps.location.pathname === path}
                  >
                    {title}
                  </Nav.Link>
                )}
              </Location>
            ))}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};
export default Navigation;
