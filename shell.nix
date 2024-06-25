with import <nixpkgs> {};

let
  sources = import ./nix/sources.nix;
in mkShell {
  nativeBuildInputs = [
    espeak
    pulseaudio
    qt5.qttools.dev
    python3Packages.autopep8
    python3Packages.flake8
    python3Packages.gtts
  ];

  propagatedBuildInputs = [
    (python3.withPackages (ps: with ps; [
      pydbus
      pyqt5
      gtts
    ]))
  ];

  # Normally set by the wrapper, but we can't use it in nix-shell (?).
  QT_QPA_PLATFORM_PLUGIN_PATH="${qt5.qtbase.bin}/lib/qt-${qt5.qtbase.version}/plugins";
}