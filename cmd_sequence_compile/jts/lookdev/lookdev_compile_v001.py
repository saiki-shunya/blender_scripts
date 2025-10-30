ffmpeg -y -framerate 24 -start_number 1 -i JTS_lookdev_008_%04d.png -frames:v 320 `
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p `
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart `
  JTS_lookdev_008.mp4