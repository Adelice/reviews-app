import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col, Card, Button, Modal } from 'react-bootstrap';

function BodySection() {
  const tmdbApiKey = '37b6a378f10e5a19a9f9d40c5a1b0fb5';
  const googleBooksApiKey = 'AIzaSyAuzbJr7axrcL_C9V0Ph0GQxEx1OFod42o'; // Replace with your actual API key
  const tmdbEndpoint = `https://api.themoviedb.org/3/movie/popular?api_key=${tmdbApiKey}&language=en-US&page=1`;
  const googleBooksEndpoint = `https://www.googleapis.com/books/v1/volumes?q=javascript&key=${googleBooksApiKey}`;
  const [movies, setMovies] = useState([]);
  const [books, setBooks] = useState([]);
  const [selectedItem, setSelectedItem] = useState(null);

  useEffect(() => {
    // Fetch movies from TMDB API
    fetch(tmdbEndpoint)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => setMovies(data.results.slice(0, 4))) // Limit to 4 items
      .catch(error => console.error('Error fetching movie data:', error));

    // Fetch books from Google Books API
    fetch(googleBooksEndpoint)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => setBooks(data.items.slice(0, 4))) // Limit to 4 items
      .catch(error => console.error('Error fetching book data:', error));
  }, [tmdbEndpoint, googleBooksEndpoint]);

  const trimText = (text, maxLength) => {
    if (text.length <= maxLength) {
      return text;
    }
    return text.substring(0, maxLength) + '...';
  };

  const handleItemClick = item => {
    setSelectedItem(item);
  };

  const handleClose = () => {
    setSelectedItem(null);
  };

  const renderTitle = (title, maxLength) => {
    if (title.length <= maxLength) {
      return title;
    }
    return (
      <span title={title}>
        {title.substring(0, maxLength)}...
      </span>
    );
  };

  return (
    <Container className="mt-4 text-center">
      <h2>Popular Items</h2>
      <Row>
        {/* Display Movies */}
        {movies.map(movie => (
          <Col key={movie.id} xs={12} md={6} lg={4} xl={3}>
            <Card className="mb-3" onClick={() => handleItemClick(movie)}>
              <Card.Img
                variant="top"
                src={`https://image.tmdb.org/t/p/w500/${movie.poster_path}`}
                style={{ height: '400px', objectFit: 'cover' }} // Set a fixed height for uniformity
              />
              <Card.Body>
                <Card.Title style={{ fontSize: '16px', textAlign: 'center' }}>
                  {renderTitle(movie.title, 18)}
                </Card.Title>
                <Card.Text style={{ textAlign: 'left' }}>{trimText(movie.overview, 150)}</Card.Text>
              </Card.Body>
            </Card>
          </Col>
        ))}

        {/* Display Books */}
        {books.map(book => (
          <Col key={book.id} xs={12} md={6} lg={4} xl={3}>
            <Card className="mb-3" onClick={() => handleItemClick(book)}>
              <Card.Img
                variant="top"
                src={book.volumeInfo.imageLinks.thumbnail}
                alt={book.volumeInfo.title}
                style={{ height: '400px', objectFit: 'cover' }} // Set a fixed height for uniformity
              />
              <Card.Body>
                <Card.Title style={{ fontSize: '16px', textAlign: 'center' }}>
                  {renderTitle(book.volumeInfo.title, 18)}
                </Card.Title>
                <Card.Text style={{ textAlign: 'left' }}>{trimText(book.volumeInfo.description, 150)}</Card.Text>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      {/* Modal for detailed information */}
      {selectedItem && (
        <Modal show={!!selectedItem} onHide={handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>{selectedItem.title || selectedItem.volumeInfo.title}</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <p>{selectedItem.overview || selectedItem.volumeInfo.description}</p>
            {/* Add more details as needed */}
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleClose}>
              Close
            </Button>
          </Modal.Footer>
        </Modal>
      )}
    </Container>
  );
}

export default BodySection;
