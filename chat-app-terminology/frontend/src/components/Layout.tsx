import * as React from "react";
import { Container, Navbar, Nav } from "react-bootstrap";
import type { PageProps } from "gatsby";

interface LayoutProps {
  children: any;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div>
      <Navbar bg="light" expand="lg">
        <Container>
          <Navbar.Brand href="#home">TermAgent</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ml-auto">
              <Nav.Link href="#about">Chat</Nav.Link>
              <Nav.Link href="#services">Terminology</Nav.Link>
              <Nav.Link href="#contact">Your development</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <div className="banner">
        <Container>{children}</Container>
      </div>
    </div>
  );
};

export default Layout;
