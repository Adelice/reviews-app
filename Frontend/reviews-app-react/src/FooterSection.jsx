import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col, Button } from 'react-bootstrap';
import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin, FaEnvelope } from 'react-icons/fa';

function FooterSection() {
  return (
    <Container fluid className="footer-container bg-secondary mt-4 p-4">
      <Row>
        {/* About Us Section (75% width) */}
        <Col xs={12} md={9}>
          <h5>About Us</h5>
          <p>
          Our love for food and cooking brought us together to create this haven for foodies, home cooks, and anyone eager to explore the joy of gastronomy. It all started with a shared passion for savoring and sharing exceptional dishes. From there, we embarked on a culinary adventure, experimenting with ingredients, techniques, and cuisines from every corner of the globe.
          </p>
        </Col>

        {/* Contact Us Section (25% width) */}
        <Col xs={12} md={3} className="text-center">
          <h5>Contact Us</h5>
          <div className="social-icons">
            <Button variant="outline-dark" className="m-1">
              <FaFacebook />
            </Button>
            <Button variant="outline-dark" className="m-1">
              <FaTwitter />
            </Button>
            <Button variant="outline-dark" className="m-1">
              <FaInstagram />
            </Button>
            <Button variant="outline-dark" className="m-1">
              <FaLinkedin />
            </Button>
            <Button variant="outline-dark" className="m-1">
              <FaEnvelope />
            </Button>
          </div>
        </Col>
      </Row>
    </Container>
  );
}

export default FooterSection;
