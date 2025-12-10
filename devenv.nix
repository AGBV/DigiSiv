{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  packages = with pkgs; [
    git
    uv
  ];

  processes = {
    streamlit.exec = "uv run streamlit run app.py";
    jupyter.exec = "uv run jupyter notebook";
  };

  scripts = {
    # streamlit.exec = ''uv run streamlit "$@"'';
    jupyter.exec = ''uv run jupyter "$@"'';
  };

  enterShell = ''
    if [ ! -L "$DEVENV_ROOT/.venv" ]; then
        ln -s "$DEVENV_STATE/venv/" "$DEVENV_ROOT/.venv"
    fi
  '';

  languages.python = {
    enable = true;

    uv = {
      enable = true;
      sync = {
        enable = true;
        groups = [
          # "test"
          # "docs"
        ];
      };
    };

    libraries = with pkgs; [
      zlib
      glib.out
    ];
  };
}
