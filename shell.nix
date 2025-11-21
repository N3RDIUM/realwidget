{ pkgs ? import <nixpkgs> {} }:

let
    hyprland-py-src = pkgs.fetchgit {
        url = "https://github.com/hyprland-community/hyprland-py";
        rev = "HEAD";
        sha256 = "sha256-R26w6ot/gVBEx8yVbRA6ZPTUvCLLXFNrebTzvYClx40=";
    };
in

pkgs.mkShell {
    buildInputs = [
        pkgs.python313
        (pkgs.python313.withPackages (ps: with ps; [
            flask
            flask-socketio
            python-engineio
            python-socketio
        ]))
    ];

    PYTHONPATH = "${hyprland-py-src}:${pkgs.python313.sitePackages}";
}
