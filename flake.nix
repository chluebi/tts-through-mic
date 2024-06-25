{
  description = "Application packaged using poetry2nix";

  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
      in
      {
        packages = {
          default = mkPoetryApplication { 
            projectDir = self; 
            nativeBuildInputs = [
              pkgs.qt5.qtbase.dev
              pkgs.qt5.qttools.dev
              pkgs.kdeFrameworks.kglobalaccel
              pkgs.pipewire
              pkgs.espeak-ng
            ];
          };
        };

        devShells.default = pkgs.mkShell {
          inputsFrom = [ self.packages.${system}.default ];
          packages = [ 
            pkgs.poetry
            pkgs.qt5.qtbase.dev
            pkgs.qt5.qttools.dev
            pkgs.kdeFrameworks.kglobalaccel
            pkgs.pipewire
            pkgs.espeak-ng
          ];
        };

        checks = {
          pytest =
            self.packages.${system}.default.overrideAttrs
              (oldAttrs: {
                name = "check-${oldAttrs.name}";
                doCheck = true;
                checkPhase = "pytest";
              });
        };
      });
}