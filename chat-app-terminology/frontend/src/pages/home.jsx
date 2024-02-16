import * as React from "react"; 
import { Container, Navbar, Nav, Button } from "react-bootstrap"; 

const IndexPage = () => { 
	return ( 
		<div> 
			<Navbar bg="light"
					expand="lg"> 
				<Container> 
					<Navbar.Brand href="#home"> 
						TermAgent 
					</Navbar.Brand> 
					<Navbar.Toggle aria-controls="basic-navbar-nav" /> 
					<Navbar.Collapse id="basic-navbar-nav"> 
						<Nav className="ml-auto"> 
							<Nav.Link href="#about">About</Nav.Link> 
							<Nav.Link href="#services">Services</Nav.Link> 
							<Nav.Link href="#contact">Contact</Nav.Link> 
						</Nav> 
					</Navbar.Collapse> 
				</Container> 
			</Navbar> 
			<div className="banner"> 
				<Container> 
					<h1> 
						Welcome to My Website using 
						Gatsby and React Boostrap 
					</h1> 
					<Button variant="primary"
							href="#services"> 
						Explore 
					</Button> 
				</Container> 
			</div> 
		</div> 
	); 
}; 

export default IndexPage; 
export const Head = () => ( 
	<title>Home Page</title> 
);
