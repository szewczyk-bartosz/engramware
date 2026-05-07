{
  inputs.nixpkgs.url = "nixpkgs/nixos-unstable";

  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    python = pkgs.python313;
  in {
    packages.${system} = {
      bmd = pkgs.stdenv.mkDerivation {
        pname = "bmd";
        version = "0.1.0";
        src = ./.;

        installPhase = ''
          mkdir -p $out/${python.sitePackages}
          cp -r bmd $out/${python.sitePackages}/

          mkdir -p $out/bin
          cat > $out/bin/bmd <<EOF
          #!${python}/bin/python
          import sys
          sys.path.insert(0, "$out/${python.sitePackages}")
          from bmd.cli import main
          sys.exit(main())
          EOF
          chmod +x $out/bin/bmd
        '';
      };

      default = self.packages.${system}.bmd;
    };
  };
}
