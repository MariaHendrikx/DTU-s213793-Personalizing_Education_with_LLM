import * as React from "react";
import type { HeadFC, PageProps } from "gatsby";
import Layout from "../components/Layout";
import RightPanel from "../components/RightPanel";
import LeftPanel from "../components/LeftPanel";
import MiddlePanel from "../components/MiddlePanel";
import {Container, Row, Col} from 'react-bootstrap';

interface LayoutProps {
  children: any;
}

const IndexPage: React.FC<LayoutProps> = ({children}) => {
  return (
  <Layout >
    <Container>
      <Row >
        <Col sm={3}><LeftPanel children={undefined}></LeftPanel></Col>
        <Col sm={6}><MiddlePanel children={undefined}></MiddlePanel></Col>
        <Col sm={3}><RightPanel children={undefined}></RightPanel></Col>
      </Row>
    </Container>
  </Layout>
  );
};


export default IndexPage;
export const Head: HeadFC = () => <title>Home Page</title>;