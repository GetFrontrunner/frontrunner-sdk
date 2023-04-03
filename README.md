# Frontrunner SDK

[Frontrunner][frontrunner] is the first zero gas fee, decentralized sports
prediction market built on blockchain where you get the best odds with no house
edge.

[frontrunner]: https://www.getfrontrunner.com/

This is an SDK which allows you to interact with our public-facing API easily
via Python.

## Developer

Note: this assumes OSX

### Prerequisite Installation

Install [`brew`][brew]. This will be used to install other required tooling.

[brew]: https://brew.sh/

Install [Visual Studio Code][vscode]. This repository has configuration for
vscode to make the development experience uniform and smooth for everyone.

[vscode]: https://code.visualstudio.com/

```sh
brew install --cask visual-studio-code
```

Install [`pants`][pants]. Pants is a generic build tool that supports multiple
languages and tools. Both local builds and CI builds use Pants.

[pants]: https://www.pantsbuild.org/docs/welcome-to-pants

```sh
brew install pantsbuild/tap/pants
```

Clone the repository. Then, open up the repository in vscode.
[Install the recommended extensions][install-recommended-extensions] for this
workspace. Restart vscode.

[install-recommended-extensions]: https://code.visualstudio.com/docs/editor/extension-marketplace#_workspace-recommended-extensions

In a terminal at the root of the repository, test your setup by running...

```sh
pants lint ::
pants check ::
pants test ::
```

To make vscode use the correct Python environment, in a terminal, run...

```sh
pants export ::
```

To activate the virtual environment in a shell, run...

```sh
bash ./dist/export/python/virtualenv/3.8.16/bin/activate
```

### Codegen

Generate Python code using the remote `openapi.json` and [swagger-codegen][swagger-codegen].

[swagger-codegen]: https://github.com/swagger-api/swagger-codegen

#### Installation

```sh
brew install swagger-codegen
```

#### Adding a Client

1. Add a dir under `openapi`
2. Put the API's `openapi.json` in that directory
3. Run `./scripts/codegen.sh`

#### Getting Help

To see additional options:

```sh
swagger-codegen generate --help
swagger-codegen config-help -l python
```

### Running Tests

To test everything, run...

```sh
pants test ::
```

To test a single file, run...

```sh
pants test --no-use-coverage ${file}
```

### Local Testing via REPL

To get a Python shell to test code, run...

```sh
pants repl ::
```
