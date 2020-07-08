import React from "react";
import { Container, Nav, Navbar } from "react-bootstrap";
import { Link } from "gatsby";
import { Location } from "@reach/router";
import { isExternalPath } from "../utils";
import useNavigationConfig from "../../hooks/useNavigationConfig";

interface NavBarLinks {
  title: string;
  path: string;
}

const Navigation: React.FC = () => {
  const { links: navbarLinks } = useNavigationConfig();

  return (
    <Navbar collapseOnSelect expand="md" bg="dark" variant="dark" sticky="top">
      <Container>
        <Navbar.Brand>
          <Link to="/">
            <img
              src="/assets/logo.png"
              height="30"
              className="d-inline-block align-top"
              alt="Nitratine Logo"
            />
          </Link>
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
                    as={isExternalPath(path) ? undefined : Link}
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
