# Font Algorithm

Load engine
Load ui
Init ui

During ui.Init or ui_restart
Check if atlas image exists
  yes : Register atlas
  no  : Generate atlas

Register atlas
  Check correct size
    no  : Generate it
  Register font image
  Load     font data

Generate atlas
  Load ft2
  Load face
  Store glyph data (bitmap, grid position, size)
  Generate atlas buffer
    Populate tga header
    Write glyphs into atlas
