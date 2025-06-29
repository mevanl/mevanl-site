---
title: Log 1 - Initial Start
date: 2025-06-28
summary: Start of project, using satellite map, political borders
---

Repo Commit at the time of writing: [here](https://github.com/mevanl/stratmap/tree/efcd6585a2fdcb43437e46e91b5fb92d5cf62374)

## Step 1: Getting a Map
As lined out in the plan devlog posted yesterday, the first step was having a satellite map to be rendered and be able to pan, zoom, etc. 

Thankfully, there are plently of open-source libraries and data out there to choose from that I can use to accomplish this. I ended up using the popular MapLibre library since the documentation and examples you can find are great and it is very easy to hit the ground running with it. (It also has MapLibre Native, which is a C++ library that can be used with non-web applications, so that is an avenue that we might venture down later in the project.)

Getting started with MapLibre is as easy as a single npm install 
```bash
npm install maplibre-gl
```

After that, You just have to create a div for the map to live in inside your html:
```html
<div id="map"></div>
```

Some CSS to tell it to use the entire screen
```css
#map {
  width: 100vw;
  height: 100vh;
}
```

Then just define your map in the script you import into the HTML:
```js
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json',
  center: [0, 0],
  zoom: 2
});
```

That is all it takes to render and display a map onto the screen! Not even 15 lines of code. This works fine for what it is, however if we want to build a system, we will need to implement some architecture to seperate out our code into useful modules instead of one big main file. 

Inside my source folder:
```
.
├── main.js
├── map
│   ├── config
│   │   └── mapStyle.json
│   ├── layers
│   │   ├── plans.js
│   │   ├── political.js
│   │   └── units.js
│   ├── mapManager.js
│   └── utils
└── style.css
```

This makes it so the map logic is self-contained, and main can just call functions from the mapManager and change layer visibility as needed. 

## Step 2: Map Styles
A map style is a json file that defines everything about a map's appearance. 

In the earlier example, we are using a map that has borders and land, but is not satellite based, being more akin to a streetview map. To change this, we must edit the source of our map to be satellite based. I landed on using Esri's map since it is very high quality and free to use. To use it, I just have to change out the sources and layers in the mapStyle.json file and tell the map to use it. 
```json
{
    "version": 8,
    "sources": {
      "esri": {
        "type": "raster",
        "tiles": [
          "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        ],
        "tileSize": 256,
        "attribution": "Tiles © Esri — Source: Esri, Earthstar Geographics"
      }
    },
    "layers": [
      {
        "id": "esri-tiles",
        "type": "raster",
        "source": "esri",
        "minzoom": 0,
        "maxzoom": 24
      }
    ]
  }
``` 

## Step 3: Layers
Adding layers is pretty simple thanks to MapLibre. Without it, you would have to manually edit the map style json to change the apperance of the map. The first layer we would like to add is a simple border between the countries. First, I had to find a place to get the lines that we can use. I found using https://geojson-maps.kyd.au/ to be simple and easy, making sure to use the highest resolution and all regions of the world. 

After downloading the resulting json file, all I had to do was fetch it and tell my map to use it. We first have to add the source to the map, just like we did with the tiles. I just called this source political and gave it a type of geojson (that is the format of the data), and added a layer using that source that is a simple line.
```js
export function loadPoliticalMapLayer(map) {
    fetch('/data/political.geojson')
    .then(res => res.json())
    .then(data => {
        map.addSource('political', {
            type: 'geojson',
            data
        })
    
        map.addLayer({
            id: 'political-border-line',
            type: 'line',
            source: 'political',
            paint: {
                'line-color': '#000000',
                'line-width': 1
            }
        })
    })
}
```

Calling this function after the map was loaded, we have country borders! This will be a pattern for pretty much all layers. We will need to add new sources with data and then tell layers to use that data.

## Conclusion 
I have found working with MapLibre to be extremely easy. When initially researching, I thought that I might have to create an system for managing the style json, but MapLibre does that for us. Progress is fast and you get instant visual feedback, making it quick fun to work on. The more interesting parts of the project will come when we get to the user placing markers, units, etc. and saving and loading state. I currently have a simple button to toggle the political layer, however I will have to create some pretty buttons and an island for them so that it doesnt look awful. Thanks for reading!

