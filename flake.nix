{
  description = "Web Services";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-25.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};
        mongodb-bin = pkgs.stdenv.mkDerivation {
          name = "mongodb-bin";
          src = pkgs.fetchurl {
            url = "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2404-8.2.4.tgz";
            hash = "sha256-8yd+ehD83mvRSpZIEnEsK3hTrVEt8Mlp5nzhE/Hs/2g=";
          };

          nativeBuildInputs = [pkgs.autoPatchelfHook];
          buildInputs = with pkgs; [curl libgcc openssl];

          installPhase = ''
            mkdir -p $out/bin
            install -Dt $out/bin bin/mongod bin/mongos
          '';
        };
      in {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            (python3.withPackages (ps: [ps.flask ps.requests ps.pymongo]))
            mongodb-bin
          ];
        };
      }
    );
}
