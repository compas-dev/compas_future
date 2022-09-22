# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

* Added `Mesh.vertex_point`.
* Added `Mesh.edge_start`.
* Added `Mesh.edge_end`.
* Added `Mesh.edge_line`.
* Added `Mesh.face_polygon`.
* Added `Mesh.face_plane`.
* Added `Mesh.halfedge_loop_vertices`.
* Added `Mesh.halfedge_strip_faces`.

### Changed

* Changed `Mesh.vertex_normal` to return `Vector`.
* Changed `Mesh.edge_vector` to return `Vector`.
* Changed `Mesh.edge_direction` to return `Vector`.
* Changed `Mesh.face_centroid` to return `Point`.
* Changed `Mesh.face_normal` to return `Vector`.

### Removed

