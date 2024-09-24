# Timing Notes

This document summarizes timing information of various configurations of the
rendering pipeline.

## Rendering Steps

The timing for the steps performed consist of the following:

* Render:         Time to push blocks through the OpenGL rendering pipeline
* ReadFromOpenGL: Time to read the image generated from OpenGL
* Convert:        Time to convert of the image colors to BlockID maps
* Summary:        Time to generate summary of blocks

Details of configurations used and results are provided in the remaining subsections

## Timing Results

Experiments were run by rendering over 100 random poses within the Sparky map.  Results of each step of the rendering pipeline are summarized in the following subsections.  Results listed are in milliseconds.


### Render

Configurations:

* Initial:  Push each block into the rendering pipeline with a glBegin / glEnd pair, using GL_QUADS
* GL_TRIANGES:  Replaced GL_QUADS with GL_TRIANGLES as the OpenGL primitive used
* glDrawArray:  Use a single glDrawArray per block, instead of glBegin / glEnd
* glDrawElements:  Use glDrawElements per block, instead of glBegin / glEnd



| Configuration  | Mean Time | Std Dev |
|----------------|-----------|---------|
| Initial        | 674.504   | 110.295 |
| GL_TRIANGLES   | 721.575   |  80.177 |
| glDrawArray    | 639.026   |  48.220 |
| glDrawElements | 693.439   |  39.437 |


### Read Image

Configurations:

* Initial:  Read using 



| Configuration | Mean Time | Std Dev |
|---------------|-----------|---------|
| Initial       | 329.993   |  50.955 |



### Convert

Configurations:

* Initial:  Convert block IDs to base 256, represent the resulting 3 digits as RGB values, then convert resulting colors back to block ID.



| Configuration | Mean Time | Std Dev |
|---------------|-----------|---------|
| Initial       |   6.326   |   1.815 |



### Summarize

Configurations:

* Initial:  Read using 



| Configuration | Mean Time | Std Dev |
|---------------|-----------|---------|
| Initial       |   0.070   |   0.255 |






