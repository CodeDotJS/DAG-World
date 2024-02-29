# API Documentation

## Overview

This Flask API provides endpoints to interact with artist data collected from [DAG](https://dagworld.com) - Delhi Art Gallery. It allows users to retrieve information about artists featured on the website, including their details, images, artworks, introductions, biographies, and years of birth. Additionally, users can search for artists by name.

## Endpoints

#### Get All Artists

- **URL**: `/artists`
- **Method**: `GET`
- **Description**: Retrieves all artists from the database.
- **Response**: Returns a JSON array containing details of all artists.

---

#### Get a Random Artist

- **URL**: `/artists/random`
- **Method**: `GET`
- **Description**: Retrieves a random artist from the database.
- **Response**: Returns JSON data representing a random artist.

---

#### Get Multiple Random Artists

- **URL**: `/artists/random/{number}`
- **Method**: `GET`
- **Description**: Retrieves multiple random artists from the database.
- **Parameters**:
  - `number` (integer): Number of random artists to retrieve.
- **Response**: Returns a JSON array containing details of the specified number of random artists.

---

#### Get Artist by Name

- **URL**: `/artist/{artist_name}`
- **Method**: `GET`
- **Description**: Retrieves details of a specific artist by name.
- **Parameters**:
  - `artist_name` (string): Name of the artist.
- **Response**: Returns JSON data representing the artist details.

---

#### Get Artist Introduction

- **URL**: `/artist/{artist_name}/intro`
- **Method**: `GET`
- **Description**: Retrieves the introduction of a specific artist by name.
- **Parameters**:
  - `artist_name` (string): Name of the artist.
- **Response**: Returns JSON data containing the introduction of the artist.

---

#### Get Artist Biography

- **URL**: `/artist/{artist_name}/bio`
- **Method**: `GET`
- **Description**: Retrieves the biography of a specific artist by name.
- **Parameters**:
  - `artist_name` (string): Name of the artist.
- **Response**: Returns JSON data containing the biography of the artist.

---

#### Get Artist Year of Birth

- **URL**: `/artist/{artist_name}/year`
- **Method**: `GET`
- **Description**: Retrieves the year of birth of a specific artist by name.
- **Parameters**:
  - `artist_name` (string): Name of the artist.
- **Response**: Returns JSON data containing the year of birth of the artist.

---

#### Get Artist Image

- **URL**: `/artist/{artist_name}/image`
- **Method**: `GET`
- **Description**: Retrieves the image of a specific artist by name.
- **Parameters**:
  - `artist_name` (string): Name of the artist.
- **Response**: Returns JSON data containing the image URL of the artist.

---

#### Get Artist Artworks

- **URL**: `/artist/{artist_name}/artworks`
- **Method**: `GET`
- **Description**: Retrieves all artworks of a specific artist by name.
- **Parameters**:
  - `artist_name` (string): Name of the artist.
- **Response**: Returns a JSON array containing details of all artworks by the artist.

---

#### Search Artists by Name

- **URL**: `/artists/search/{query}`
- **Method**: `GET`
- **Description**: Searches for artists by name.
- **Parameters**:
  - `query` (string): Search query for artist names.
- **Response**: Returns a JSON array containing details of artists matching the search query.
