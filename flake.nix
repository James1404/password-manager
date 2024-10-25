{
  description = "Password Manager";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, flake-utils, nixpkgs, ... }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let pkgs = import nixpkgs { inherit system; }; in
        {
          devShells.default = pkgs.mkShell {
            packages = with pkgs; [
              (python312.withPackages (python-pkgs: with python-pkgs; [
                debugpy
              ]))
              pyright
            ];
          };
        }
      );
}
