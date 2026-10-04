# Native Apple Silicon compatibility

This branch starts at upstream commit `f8fe432101fb1852f8c4d8546504a5278f6ef57f`.
It contains the three source fixes used in a tested AppleClang ARM64 installation:

- `BufferImage` obtains dimensions through its existing `numCols()` and
  `numLines()` methods.
- Poisson vertex subtraction uses `point`, the member actually declared by the
  oriented and color vertex types.
- `SparseMatrix::SetZero()` resets the current number of rows through the
  existing row-based `Resize()` API.

These are CPU build fixes. They do not implement Metal acceleration, change
photogrammetry thresholds, or establish reconstruction accuracy. Original source
copyright and license notices remain intact. No binaries or datasets are shipped.

## Build

Install Xcode Command Line Tools, CMake and Python 3. Start from a clean checkout;
never reuse build caches generated on Linux or another source revision. A
headless build needs neither Qt nor X11. From the checkout root:

```sh
cmake -S . -B build-macos-arm64 \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_OSX_ARCHITECTURES=arm64 \
  -DGIT_REVISION_DIST="$(git rev-parse HEAD)" \
  -DBUILD_ONLY_ELISE_MM3D=ON -DWITH_QT5=OFF -DWITH_INTERFACE=OFF \
  -DNO_X11=ON -DBUILD_POISSON=ON -DWITH_OPEN_MP=OFF \
  -DCMAKE_DISABLE_FIND_PACKAGE_OpenMP=TRUE \
  -DWITH_HEADER_PRECOMP=OFF -DWERROR=OFF -DWITH_CCACHE=OFF
cmake --build build-macos-arm64 \
  --target mm3d PoissonRecon SurfaceTrimmer --parallel 2
python3 tools/macos/test_compatibility.py
```

CMake places `mm3d` in the checkout's `bin` directory and the native mesh helpers
in `binaire-aux/darwin`. Keep those alongside `include/XML_MicMac` and
`include/XML_GEN`; moving the executable alone can break resource discovery.
The build directory is separate, but upstream still writes executable outputs
inside the source checkout. Use a dedicated checkout for each build.

## Run

```sh
python3 tools/macos/native_mm3d.py Tapioca All 'photos/.*png' 640 ByP=2 @NbMaxProc=2
python3 tools/macos/native_mm3d.py Tapas RadialBasic 'photos/.*png' Out=raw @NbMaxProc=2
python3 tools/macos/native_mm3d.py Malt -help
python3 tools/macos/native_mm3d.py C3DC -help
```

The launcher supplies `Detect=mm3d:Digeo` and `Match=mm3d:Ann` for ordinary
Tapioca matching modes unless the user supplies those options. This avoids
upstream's obsolete bundled i386 SIFT/ANN helper binaries on Apple Silicon.
Arguments remain literal, without shell expansion. Tapas still invokes the
native Apero command and the normal XML resources. Many MicMac help commands
return a nonzero code after displaying usage.

The pinned implementation was built and exercised on an Apple M1: native Tapioca
matching and Tapas-to-Apero resource loading ran; PoissonRecon and SurfaceTrimmer
processed a synthetic sphere. Twelve-view Dragon orientation failed to
initialize, so that comparison did not produce a Dragon STL. The portable test
here compiles and executes the patched Poisson subtraction/reset APIs and checks
launcher defaults and overrides; it does not reproduce a full photogrammetry run.
