Analysis of glyph images of fonts
=================================

(1) Original data creation

- Script: harfbuzz_and_crop.rb
- Output data: data

1. "Friend," "affect," "work," and "power" glyphs are rasterized for each weight of Kozuka Gothic.
2. Crop with ImageMagick.
3. Draw them in white and the background in black because applying skeletonizing  them and FFT later.

--------------------------------------------------------------------------------

(2) Skeletonization

- Script: skeletonization.sh + skeletonization.py
- Output data: skeletonization

Executed by OpenCV API. The threshold is appropriate. The heavier the weight is, the worse the quality is. There seems to be no universal threshold.

--------------------------------------------------------------------------------

(3) Magnitude spectrum calculation by fast Fourier transform

- Script: fft_and_magnitude_spectrum.py
- Output data: fft

_Magnitude spectrum_
Absolute value of coefficient of frequency decomposition by Fourier transform.

_Power spectrum_
Squared value of the magnitude spectrum.

--------------------------------------------------------------------------------

(4) Character recognition by OCR (Tesseract)

- Script: harfbuzz_and_crop_for_tess.rb, tesseract_test.rb, check_tess_result.rb
- Output data: data4tess

(4-1) Original data creation
harfbuzz_and_crop_for_tess.rb

(4-2) Recognition
tesseract_test.rb

(4-3) Result evaluation
check_tess_result.rb

## Further technics

- Clustering with machine learning (unsupervised).
