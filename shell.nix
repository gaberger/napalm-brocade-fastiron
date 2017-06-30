
with (import <nixpkgs> {});

stdenv.mkDerivation rec {
    name = "napalm-brocade-fastiron-${version}";
    version = "1.0";
    src = "./.";

    buildInputs = [
        (python27.withPackages (ps: with ps; [ pip virtualenv ]))
        gcc
        libffi
        openssl
    ];

    # NOTE need to export SOURCE DATE_EPOCH
    # NOTE need to escape brackets around develop because of nix variable
    # substitution
    shellHook = ''
        export SOURCE_DATE_EPOCH=$(date +%s)

        if [ ! -d "./env" ]; then
            echo -e "\nCreating virualenv in directory env ..."
            virtualenv env
        fi

        echo -e "\nActivating virualenv in directory env ..."
        source env/bin/activate

        if [ "`pip list --format=columns | grep napalm-brocade-fastiron`" == "" ]; then
            echo -e "\nInstalling napalm-brocade-fastiron in virtualenv in development mode ..."
            which pip 
            pip install -e .\[develop\] --process-dependency-links
        fi

    '';
}