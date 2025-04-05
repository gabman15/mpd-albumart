{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  };
  outputs = { self, nixpkgs, ... }@inputs: {
    packages.x86_64-linux = let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
    in rec {
      mpd-albumart = pkgs.writers.writePython3Bin "mpd-albumart" {
        libraries = with pkgs; [
          python312Packages.mpd2
        ];
        doCheck = false;
      } (builtins.readFile ./albumart.py);
      default = mpd-albumart;
    };
  };
}
