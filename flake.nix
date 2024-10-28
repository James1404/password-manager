{
  description = "Password Manager";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, flake-utils, nixpkgs, ... }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs { inherit system; };
          envWithScript = script: (pkgs.buildFHSUserEnv {
            name = "password manager";
            targetPkgs = pkgs: (with pkgs; [
              (python312.withPackages (python-pkgs: with python-pkgs; [
                debugpy
                pip
                virtualenv
                pyinstaller
              ]))
              pyright

              # qt libraries
              zstd
              glib
              libGL
              libxkbcommon
              fontconfig
              xorg.libX11
              libkrb5
              xorg.libxcb
              freetype
              dbus

              qt6.qtwayland
            ]);
            runScript = "${pkgs.writeShellScriptBin "runScript" (''
                    set -e
                    python -m venv .venv
                    source .venv/bin/activate
                    pip install -r requirements.txt
                '' + script)}/bin/runScript ";
          }).env;
        in
        {
          devShells.default = envWithScript "bash";
        }
      );
}
