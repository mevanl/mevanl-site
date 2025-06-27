---
title: StratMap Project Idea
date: 2025-06-27
summary: Covers what this project is, the scope, tech stack, etc.
---

# Overview
**StratMap** is a global visualization platform designed for military and strategic planning. It features interactive layers, real-world satellite imagery, and customizable data overlays (e.g. political boundaries, radar coverage, missile range projections). StratMap is built to simulate, analyze, and visualize global conflict scenarios and geostrategic data with clarity and precision.

# The Plan
NOTE: This is a plan, but is subject to change as development/feedback continues!

## Technical Features
* WebGL-accelerated map rendering with real-time overlays
* Toggleable layers: political, geographic, military
* GeoJSON-driven data (unit placement, scenario modeling, etc.)
* Custom icons, range rings, radar cones, trajectory arcs, and more

## Use Cases
* Strategic operations simulation
* Military planning and training tools
* Wargame scenario prototyping
* Educational/visualization tool for geopolitics and international relations

## Stack

### Frontend
* **MapLibre GL JS** for high-performance WebGL map rendering
* **Vite** for fast, modern development tooling and instant rebuilds


### Data
* **GeoJSON** for political boundaries, unit placement, radar zones, and trajectory overlays
* Geographic data sources: **Natural Earth**, **GADM**, or custom datasets
* Modular structure for layer loading and toggling

### Backend
StratMap is entirely frontend-driven and designed to be **stateless**. There is no user authentication, database, or cloud storage. All scenario data lives in the browser and can be exported/imported as `.json` files. The app will be deployed as a static site.

If heavier simulations are needed in the future (e.g. missile trajectory calculations or radar detection), they may be handled via **WASM written in Zig**, running entirely client-side.

# Roadmap
1. Interactive satellite map (MapLibre)
2. Toggleable political layer (GeoJSON)
3. Unit & symbol placement (icons, arrows, city markers, etc.)
4. Adjustable borders (territorial exchange simulation)
5. Local scenario saving/loading (export/import JSON)
6. Range rings, radar zones, and detection overlays
7. Missile trajectory visualization
8. _(Stretch)_ In-browser simulation engine via WebAssembly (Zig)
