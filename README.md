# ghs

simple gh star lists viewer/opener/downloader

<img src="assets/demo.gif" height="400">

## locally

```bash
# edit GH_UNAME & HOME_PATH @ cfg.py
# frist run creates a .json with gh stars

pixi run ghs
-u, --update  overwrites json file
-c, --cwd     sets clone path to cwd
-l, --log     prints json and exits
--help        Show this message and exit.
```

## globally

the following pixi-global.toml works, taking the current state of pixi regarding global tools [1](https://github.com/prefix-dev/pixi/issues/565#issuecomment-1873720212) [2](https://github.com/prefix-dev/pixi/milestone/9)

```bash
## @ ~/.pixi/manifests/pixi-global.toml
pixi global edit
```

```toml
[envs.ghs]
channels = ["conda-forge"]
dependencies = { ghs = { git = "https://github.com/zuble/ghs" }, inquirerpy = { git = "https://github.com/zuble/InquirerPy" }, click = "*", pyrootutils = "*", requests = "*", rich = "*", bs4 = "*", prompt-toolkit = "*", pfzy = "*"}
exposed = { ghs = "ghs" }
```

```bash
pixi global update ghs
which ghs && type ghs
## either move .json to @ ~/.local/share/ghs
## or let frist run populate
ghs --help
```
