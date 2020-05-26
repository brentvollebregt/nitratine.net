import React from "react";
import { Container, Nav, Navbar } from "react-bootstrap";
import { Link } from "gatsby";

const navbarLinks = [
  {
    path: "/",
    title: "Home"
  },
  {
    path: "/blog",
    title: "Blog"
  },
  {
    path: "https://www.youtube.com/c/PyTutorials",
    title: "YouTube"
  },
  {
    path: "https://github.com/brentvollebregt",
    title: "GitHub"
  },
  {
    path: "/about",
    title: "About"
  }
];

const Navigation = () => (
  <Navbar collapseOnSelect expand="md" bg="dark" variant="dark" sticky="top">
    <Container>
      <Navbar.Brand>
        <img
          src="/img/logo.png"
          height="30"
          className="d-inline-block align-top"
          alt="Nitratine Logo"
          style={{ cursor: "pointer" }}
        />
      </Navbar.Brand>
      <Navbar.Toggle aria-controls="responsive-navbar-nav" />
      <Navbar.Collapse id="responsive-navbar-nav">
        <Nav className="mr-auto">
          {navbarLinks.map(({ path, title }) =>
            path.startsWith("http://") || path.startsWith("https://") ? (
              <Nav.Link
                key={path}
                href={path}
                /* TODO Remove window.location.pathname */
                active={window.location.pathname === path}
              >
                {title}
              </Nav.Link>
            ) : (
              <Nav.Link
                key={path}
                /* TODO Remove window.location.pathname */
                active={window.location.pathname === path}
                as={Link}
                to={path}
              >
                {title}
              </Nav.Link>
            )
          )}
        </Nav>
      </Navbar.Collapse>
    </Container>
  </Navbar>
);

export default Navigation;
